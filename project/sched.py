from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import User, Schedule, Event
from datetime import datetime
from counter import Counter

#TODO counter for schedules will be from 50000 upwards
#counter for events is 60000 upwards

sched = Blueprint('sched', __name__)

scheduleAssign = Counter(50003)
#not sure if needed, keep for now
eventAssign = Counter(60000)


@sched.route('/schedules')
def schedules():
    schedules = Schedule.query.order_by(Schedule.scheduleId).all()

    return render_template('schedules.html', schedules = schedules, count = scheduleAssign.get())

#placeholder for accessing schedule, will redirect to new page containing said schedule
@sched.route('/schedules/<int:param>//')
def scheduleAtId(param):

    #gets schedule with id param
    sched = Schedule.query.filter_by(scheduleId=param).first()
    evnts = Event.query.filter_by(scheduleId=param)

    if not sched:
        return 'placeholder text for schedule not found'

    return render_template('schedule.html', schedule = sched, events = evnts)

#get all events
@sched.route('/events')
def events():
    return render_template('events.html')

@sched.route('/schedules/<int:schedId>/createevent')
def createEvent(schedId):

    schedule = Schedule.query.filter_by(scheduleId=schedId).first()

    if not schedule:
        flash(Markup('schedule does not exist. why not try checking out <a href = "/schedules" class="alert-link"> the currently available ones? </a>'))
        return 'schedule no exist'


    return render_template('createevent.html')

@sched.route('/createschedule')
def createSched():
    return render_template('createschedule.html')

#time ends up being formatted wrong, changes that

def filterTime(datestring):
    datestring = str(datestring)
    return datestring.replace('T', ' ')


@sched.route('/schedules', methods = ['POST'])
def insertSched():

    name = request.form.get('name')
    start = request.form.get('sDate')
    end = request.form.get('eDate')

    if name is None:
        flash('yuh')
        return redirect(url_for('sched.createSched'))

    if start is None:
        flash ('wtf')
        return redirect(url_for('sched.createSched'))
    
    #somehow not working???
    if end is None:
        flash('uhhhh')
        return redirect(url_for('sched.createSched'))

    startStr = str(start)
    endStr = str(end)


    #convert to dateTime
    dateFormat = '%Y-%m-%dT%H:%M'
    startD = datetime.strptime(startStr, dateFormat)
    endD = datetime.strptime(endStr, dateFormat)

    

    startSeconds = startD.timestamp()
    endSeconds = endD.timestamp()

    if  (startSeconds - endSeconds) > 3600:
        flash('At least have one hour between start and end time')
        return redirect(url_for('sched.createSched'))

    #using id 1 as placeholder for now
    new = Schedule(1, scheduleAssign.get(), name, startD, endD)

    scheduleAssign.increment()

    db.session.add(new)
    db.session.commit()

    return redirect(url_for('sched.schedules'))

sched.route('/events', methods = ['POST'])
def insertEvent():

    name = request.form.get('name')
    activity = request.form.get('activity')
    #get attractionID through some kind of search

    startTime = request.form.get('st')
    endTime = request.form.get('et')

    startSeconds = startTime.timestamp()
    endSeconds = endTime.timestamp()

    if  (startTime.year == endTime.year) and (startTime.month == endTime.month) and (startTime.day == endTime.day) and (startTime.hour == endTime.hour) and ((startTime.minute - endTime.minute) > 30):
        flash('overlap')
        return redirect(url_for('sched.createEvent'))
    
    return redirect(url_for('sched.events'))