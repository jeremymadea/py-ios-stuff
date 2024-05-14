# coding: utf-8

# NOTE: When you run this script, you will be prompted to allow access to your reminders. The script will (obviously) not work correctly if you deny this permission. You can change Pythonista's permissions from the Settings app.

import arrow # migrate from datetime etc.
import console
from datetime import datetime, timezone, timedelta
from dialogs import alert
import math
import os
import reminders
import shelve
import sqlite3
import sys

mm_cal_name = 'MedMaster'
mm_cal = None
mm_url = None 
mm_shelf_file = 'MedMaster_appdata'
mm_db_file = 'MedMaster.db'

# seconds late or early a med can be taken and 
# still considered on time
mm_on_time = 1800 


######## class definitions

class DosingPolicy:
	def __init__(self, interval, on_time=mm_on_time):
		self.rx_interval = interval 
		self.on_time = on_time

	def check(self, interval):
		diff = self.rx_interval - interval
		adiff = abs(diff) # absolute
		rdiff = fmt_interval(adiff) # readable

		if adiff <= self.on_time: 
			mesg = 'on time'
		elif diff < 0:
			mesg = rdiff + ' late'
		else:
			mesg = rdiff + ' early'
			
		return { 
			 'diff': diff,
			 'adiff': adiff,
			 'mesg': mesg,
		}
		
### end DosingPolicy class		
		
		
class Medication:
	def __init__(self, med, cal):
		if isinstance(med, str): 
			med = db_get_med(med)		 
		self.name = med['name']
		self.interval = med['interval']
		self.policy = DosingPolicy(self.interval)
		self.cal = cal
		self.get_last_dose()
		
	def get_last_dose(self):		
		self.last_dose = db_get_last_log(self.name)
		if self.last_dose is not None:
			self.check_timing(self.last_dose['delta'])
			
	def add_reminder(self):
		r = reminders.Reminder(self.cal)
		r.title = self.name
		r.url = f'pythonista3://MyScripts/MedMaster/MedMaster.py?action=run&args=take%20{self.name}'
		r.notes = r.url
	  	
		# Migrate to arrow
		# due = arrow.now().shift(seconds=self.interval)
		# Previous datetime code
		due = datetime.now() + timedelta(seconds=self.interval)
		r.due_date = due
		a = reminders.Alarm()
		a.date = due
		r.alarms = [a]
		r.save()
		
	def add_reminder_from_last_dose(self):
		if self.last_dose is None:
			pribt('error: no last dose')
			return None
		r = reminders.Reminder(self.cal)
		r.title = self.name
		r.url = f'pythonista3://MyScripts/MedMaster/MedMaster.py?action=run&args=take%20{self.name}'
		r.notes = r.url
	  	
		# Migrate to arrow
		# due = arrow.now().shift(seconds=self.interval)
		# Previous datetime code
		due = datetime.fromisoformat(self.last_dose['lts']) + timedelta(seconds=self.interval) 
		r.due_date = due
		a = reminders.Alarm()
		a.date = due
		r.alarms = [a]
		r.save()	
		
	def del_reminder(self):
		rems = reminders.get_reminders(calendar=self.cal, completed=False)
		for r in rems:
			if r.title == self.name:
				deleted = reminders.delete_reminder(r)
				if not deleted:
					debug_print("reminder deletion failed.")									
	def check_timing(self, interval):
		info = self.policy.check(interval) 
		self.timing_mesg = info['mesg']

	def log_dose(self):
		db_log_med(self.name)
		
		if self.last_dose is None:
			self.message = 'No previous dose in log.'
		else:
			interval = self.last_dose['delta']
			self.message = f'''Last dose was taken {fmt_interval(interval)} ago. You took this dose of {self.name} {self.timing_mesg}.
			
			'''
		self.del_reminder()
		self.add_reminder()				
		return self.message
		
	def del_dose(self):
		if self.last_dose is None:
			self.message = 'There is no previous dose to delete.'
		else:
			db_del_log_entry(self.last_dose)
			self.get_last_dose()
			self.message = 'Previous dose deleted from log.'			 
		return self.message
		
	def report(self):
		if self.last_dose is None:
			self.message = 'No previous dose in log.'
		else:
			lts = self.last_dose['lts'] # local timestamp
			interval = self.last_dose['delta']
			self.message = f'''Last dose was taken at {lts}, {fmt_interval(interval)} ago. it is now {self.timing_mesg} for the next dose of {self.name}.
			
			'''		
			rows = db_get_entries(self.name)
			for r in rows:
				print(f"{r['ts']}")
		return self.message

### end Medication class



######## 

con = sqlite3.connect(mm_db_file)
con.row_factory = sqlite3.Row
cur = con.cursor()



######## utility functions

def s2hm(s):
	h = s // 3600
	m = (s % 3600) // 60
	if (s % 60) >= 30:
		m += 1	
	if m == 60:
		m = 0
		h += 1
	return (h, m)
	
def fmt_interval(secs):
    (hrs, mins) = s2hm(secs)
    return f"{hrs} hrs and {mins} mins"



######## database utility functions 

def build_db():
	debug_print("now in build db")
	meds = [
		{'name':'oxy', 'interval': 14400 },
		{'name':'tylenol', 'interval': 28800 }
	]
	
	cur.execute('''CREATE TABLE IF NOT EXISTS med
		(name TEXT NOT NULL PRIMARY KEY, 
		interval INTEGER)
	''')
	cur.execute('''CREATE TABLE IF NOT EXISTS log
		(med TEXT, 
		 ts  DATETIME DEFAULT CURRENT_TIMESTAMP, 
		 FOREIGN KEY (med) REFERENCES med(name))
	''')

	for med in meds:
		try:
			cur.execute('''
				INSERT INTO med 
					(name, interval)
				VALUES (?, ?)
			''', 
			(med['name'], med['interval']))
		except sqlite3.IntegrityError:
			pass
	con.commit()

def db_add_new_med(name, interval):
	try:
		cur.execute('''
				INSERT INTO med 
					(name, interval)
				VALUES (?, ?)
			''', 
			(name, interval))
		print(f'Added med {name} with interval {interval}.')
	except sqlite3.IntegrityError:
		pass
	con.commit()	
	
def db_update_interval(name, interval):
	try:
		cur.execute('''
				UPDATE med 
					SET interval=?
			  WHERE NAME=?
			''', 
			(interval, name))
		print(f'Updated med {name} with interval {interval}.')
	except sqlite3.IntegrityError:
		pass
	con.commit()	
			
def db_log_med(med):
	# as a convenienxmce, this function returns 
	# secs since last log entry if it can
	# and None if it can't
	
	last_uts = db_get_log_secs(med)	
	cur.execute('''
		INSERT INTO log (med) VALUES(?);
	''', [med])
	
	con.commit()
	
	this_uts = db_get_log_secs(med)
	if last_uts is None or this_uts is None:
		return None
	return this_uts - last_uts
	
	
def db_get_log_secs(med):
	cur.execute('''
		SELECT unixepoch(ts) as uts FROM log 
		 WHERE med = ?
		 ORDER BY ts DESC LIMIT 1
	''', (med,))
	res = cur.fetchone()

	if res is None: 
		return None
		
	#debug_print(f'gls res is {dict(res)}')
	return res['uts']
	
	
# UNUSED 
def get_log(med):
	cur.execute('''
		SELECT * FROM log 
		 WHERE med = ?
		 ORDER BY ts DESC LIMIT 1
	''', [med])
	res = cur.fetchone()
	return res
	
def db_get_entries(med, secs=86400):
	cur.execute(''' 
		SELECT 
			med, 
			ts,
			datetime(ts, 'localtime') as lts,
			unixepoch(ts) as uts,
			unixepoch('now') - unixepoch(ts) as delta
		 FROM log
		WHERE med = ? 
		  AND delta < ?
		ORDER BY ts ASC
	''', (med, secs))
	rows = cur.fetchall()
	return rows
	
	
def db_get_last_log(med):
	cur.execute('''
		SELECT 
			med, 
			ts,
			datetime(ts, 'localtime') as lts,
			unixepoch(ts) as uts,
			unixepoch('now') - unixepoch(ts) as delta
		 FROM log
		WHERE med = ? 
		ORDER BY ts DESC LIMIT 1
	''', [med])
	row = cur.fetchone()
	return row
	
def db_del_log_entry(row):
	cur.execute('''
		DELETE FROM log
		WHERE med = ?
		  AND ts = ?
	''', (row['med'], row['ts']))
	con.commit()
	
	
def db_get_med(name):
	cur.execute(
		'''SELECT * FROM med
		   WHERE name=?''', [name]
	)
	m = cur.fetchone()
	return m

	
			
########  app_data utility functions	
	
def save_cal_id(id):
	with shelve.open(mm_shelf_file) as shelf:
		shelf["cal_id"] = id
		
def get_persistent(key):
	with shelve.open(mm_shelf_file) as shelf:
		val = shelf[key]
		return val
		
######## debugging utility functions
	
def debug_print(msg):
	print("DEBUG: " + f'{msg}')


					
######## Main app and auxillary functions																		
def setup_app():
	debug_print('Setting up app')
	
	debug_print('Building DB.')
	build_db()
	
	
	# find or create the reminder calendar to be 
	# used by this app. Store its unique ID in
	# in our app_data shelve store. 
	all_calendars = reminders.get_all_calendars()
	mm_cal = None
	
	for cal in all_calendars:
		if cal.title == mm_cal_name:
			mm_cal = cal
			break
	else:
		mm_cal = reminders.Calendar()
		mm_cal.title = mm_cal_name
		mm_cal.save()
		
	save_cal_id(mm_cal.identifier)
	
	
def get_last_dose_dt(med):
	# returns last dose delta time in seconds
	uts = db_get_log_secs(med)
	if uts is None:
		return None
	# migrate to arrow
	now = datetime.now(timezone.utc).timestamp()
	return int(round(now) - uts)

	
def get_interval_info(med, on_time=mm_on_time):
	
	last_dose_dt = get_last_dose_dt(med)
	
	# if there is no last dose, there is no interval 
	if last_dose_dt is None:
		return None
		
	dose_interval = fmt_interval(last_dose_dt)
	due_dt = abs(last_dose_dt - med_row['interval'])
	due_interval = fmt_interval(due_dt)
	taken = "on time"
	if due_dt > on_time:
		if last_dose_dt < med_row['interval']:
			taken = 'early'
		else:
			taken = 'late'
				
										
													
def main():
	console.clear()
	 
	if not os.path.exists(mm_shelf_file + '.db'):
		setup_app()
		
  # Retrieve the unique ID associated with the
  # calendar for this app. Then get the calendar
  # with this ID 
	cal_id = get_persistent('cal_id')
	mm_cal = reminders.get_calendar(cal_id)	

	action = None
	med = None
	
	if len(sys.argv) > 1:
		action = sys.argv[1]
	if len(sys.argv) == 3:
		med = Medication(sys.argv[2], mm_cal)
	if len(sys.argv) == 4:
		med_name = sys.argv[2]
		interval = int(sys.argv[3]) * 3600
		
	
	if action == 'init':
		setup_app()
	elif action == 'take':	
		mesg = med.log_dose()
		alert(
			f'{med.name} dose logged',
			mesg,
			'Done', hide_cancel_button=True
			)
	elif action == 'info':
		mesg = med.report()
		alert(
			f'{med.name} last dose info',
			mesg,
			'Done', hide_cancel_button=True
			)
	elif action == 'show':
		pass
	elif action == 'del': 
		### !!! TODO BUG FIX - does not fix reminders
		mesg = med.del_dose()
		mesg += '\n' + med.report()
		alert(
			f'{med.name}: DELETED LAST DOSE',
			mesg,
			'Done', hide_cancel_button=True
			)
	elif action == 'rfl': # dev utility
		med.add_reminder_from_last_dose()
	elif action == 'new':
		db_add_new_med(med_name, interval)
	elif action == 'fix': # dev utility
		db_update_interval(med_name, interval)
	else:
		pass
		
	
				
if __name__ == '__main__':
	main()
	con.close()

