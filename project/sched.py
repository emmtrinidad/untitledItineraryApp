from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from models import Attraction, Download, User, Schedule, Event
from datetime import datetime
from counter import Counter

#TODO counter for schedules will be from 50000 upwards
#counter for events is 60000 upwards

sched = Blueprint('sched', __name__)

scheduleAssign = Counter(50007)
#not sure if needed, keep for now
eventAssign = Counter(60007)



@sched.route('/schedules')
def schedules():
    schedules = Schedule.query.order_by(Schedule.scheduleId).all()

    downloadIds = []
    
    downloads = Download.query.filter_by(userId = current_user.id).all()

    for download in downloads:
        downloadIds.append(download.scheduleId)

    return render_template('schedules.html', schedules = schedules, count = scheduleAssign.get(), downloads = downloadIds)

#placeholder for accessing schedule, will redirect to new page containing said schedule
@sched.route('/schedules/<int:param>//')
def scheduleAtId(param):

    #gets schedule with id param
    sched = Schedule.query.filter_by(scheduleId=param).first()
    evnts = Event.query.filter_by(scheduleId=param)

    if not sched:
        return redirect(url_for('sched.schedules'))

    return render_template('schedule.html', schedule = sched, events = evnts)


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

@sched.route('/schedules/<int:schedId>/<int:eventId>')
@login_required
def editEventPage(eventId, schedId):

    event = Event.query.filter_by(eventId = eventId).first()

    user = current_user.get_id()
    user = User.query.filter_by(id = user).first()

    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    if not sched:
        return redirect(url_for('main.home'))

    return render_template('createevent.html', event = event, sched = sched)

@sched.route('/schedules/<int:schedId>/<int:eventId>', methods = ['POST'])
@login_required
def editEvent(eventId, schedId):

    event = Event.query.filter_by(eventId = eventId).first()

    user = current_user.get_id()
    user = User.query.filter_by(id = user).first()

    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    if not sched or not event:
        return redirect(url_for('main.home'))
    
    schedStart = sched.startDate
    schedEnd = sched.endDate

    sStartSeconds = schedStart.timestamp()
    sEndSeconds = schedEnd.timestamp()

    name = request.form.get('eventName')
    attraction = request.form.get('attraction')

    start = request.form.get('sDate')
    end = request.form.get('eDate')

    startStr = str(start)
    endStr = str(end)

    #convert to dateTime
    dateFormat = '%Y-%m-%dT%H:%M'
    startD = datetime.strptime(startStr, dateFormat)
    endD = datetime.strptime(endStr, dateFormat)

    startSeconds = startD.timestamp()
    endSeconds = endD.timestamp()

    attrac = None

    if not attraction: #attraction is not needed for event
        attrac = Attraction.query.filter_by(Address = attraction).first()
        
    if (startSeconds < sStartSeconds) or (endSeconds > sEndSeconds):
        flash('cannot be out of the time range of the schedule')
        return render_template('createevent.html', attraction = attrac, sched = sched)

    if  (startSeconds - endSeconds) > 1800:
        flash('At least have half an hour between start and end time')
        return render_template('createevent.html', attraction = attrac, sched = sched)
    
    events = Event.query.filter_by(scheduleId = sched.scheduleId).all()

    for x in events:
        
        eStart = x.startTime
        eEnd = x.endTime

        eSSeconds = eStart.timestamp()
        eESeconds = eEnd.timestamp()

        if ((endSeconds > eSSeconds and endSeconds < eESeconds) or (startSeconds > eESeconds and startSeconds < eESeconds)) and event.eventId is not x.eventId  :
            flash('Overlap between events')
            return render_template('createevent.html', attraction = attrac, sched = sched)

    
    
    event.name = name
    if event.location:
        event.location = attrac.Address
    event.startTime = startD
    event.endTime = endD
    if event.cityCode:
        event.cityCode = attrac.cityCode

    db.session.commit()

    events = Event.query.filter_by(scheduleId = sched.scheduleId).all()
    
    return render_template('schedule.html', schedule = sched, events = events)


@sched.route('/schedules/<int:schedId>/<int:eventId>/remove')
@login_required
def deleteEvent(eventId, schedId):

    user = current_user.get_id()
    user = User.query.filter_by(id = user).first()

    event = Event.query.filter_by(eventId = eventId).first()

    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    if not sched:
        return redirect(url_for('main.index'))

    if not event:
        return render_template('schedule.html', schedule = sched)

    eventAttrac = event.location
    eventName = event.name

    if user.id != event.creatorId or not user.isAdmin:
        return url_for('main.index')

    attrac = Attraction.query.filter_by(Address = eventAttrac).first()
    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    db.session.delete(event)
    db.session.commit()

    return render_template('schedule.html', sched = sched)

@sched.route('/schedules/<int:schedId>/createevent', methods = ['POST'])
@login_required 
def insertEvent(schedId):

    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    if not sched:
        return redirect(url_for('main.home'))
    
    schedStart = sched.startDate
    schedEnd = sched.endDate

    sStartSeconds = schedStart.timestamp()
    sEndSeconds = schedEnd.timestamp()

    name = request.form.get('eventName')
    attraction = request.form.get('attraction')

    start = request.form.get('sDate')
    end = request.form.get('eDate')

    startStr = str(start)
    endStr = str(end)

    #convert to dateTime
    dateFormat = '%Y-%m-%dT%H:%M'
    startD = datetime.strptime(startStr, dateFormat)
    endD = datetime.strptime(endStr, dateFormat)

    startSeconds = startD.timestamp()
    endSeconds = endD.timestamp()

    attrac = None

    if attraction:
        attrac = Attraction.query.filter_by(Address = attraction).first()
    
    if (startSeconds < sStartSeconds) or (endSeconds > sEndSeconds):
        flash('cannot be out of the time range of the schedule')
        return render_template('createevent.html', attraction = attrac, sched = sched)

    if  (startSeconds - endSeconds) > 1800:
        flash('At least have half an hour between start and end time')
        return render_template('createevent.html', attraction = attrac, sched = sched)
    
    events = Event.query.filter_by(scheduleId = sched.scheduleId).all()

    for event in events:
        
        eStart = event.startTime
        eEnd = event.endTime

        eSSeconds = eStart.timestamp()
        eESeconds = eEnd.timestamp()

        if (endSeconds > eSSeconds and endSeconds < eESeconds) or (startSeconds > eESeconds and startSeconds < eESeconds):
            flash('Overlap between events')
            return render_template('createevent.html', attraction = attrac, sched = sched)

    
    if attrac:
        new = Event(name, eventAssign.get(), current_user.get_id(), schedId, startD, endD, attrac.Address, attrac.cityCode)

    else:
        new = Event(name, eventAssign.get(), current_user.get_id(), schedId, startD, endD, None, None)

    db.session.add(new)
    db.session.commit()

    events = Event.query.filter_by(scheduleId = sched.scheduleId).all()
    
    return render_template('schedule.html', schedule = sched, events = events)

@sched.route('/schedules/<int:schedId>/createevent')
@login_required
def createEvent(schedId):

    sched = Schedule.query.filter_by(scheduleId = schedId).first()
    attraction = None

    if not sched:
        return redirect(url_for('main.home'), attraction = attraction)

    return render_template('createevent.html', sched = sched)

@sched.route('/schedules/<int:schedId>/createevent/getAttraction')
@login_required 
def createEventGetAttraction(schedId):

    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    if not sched:
        return redirect(url_for('main.home'))

    return render_template('eventsearch/attractionsearch.html', sched = sched)

@sched.route('/schedules/<int:schedId>/createevent/getAttraction', methods = ['POST'])
@login_required 
def createEventSearchedAttraction(schedId):

    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    if not sched:
        return redirect(url_for('main.home'))
    
    check = request.form.get('search')
    attrac = Attraction.query.filter(Attraction.Name.contains(check)).all()

    return render_template('eventsearch/attractionresults.html', attractions = attrac, sched = sched)

@sched.route('/schedules/<int:schedId>/createevent/getAttraction/<string:address>')
def createEventAttractionSelected(schedId, address):

    sched = Schedule.query.filter_by(scheduleId = schedId).first()
    attraction = Attraction.query.filter_by(Address = address).first()

    return render_template('createevent.html', attraction = attraction, sched = sched)

@sched.route('/downloads')
@login_required #user needs to be logged in in order to actually check downloads
def getDownloads():

    check = current_user.get_id()

    downloads = Download.query.filter_by(userId = check).all() #get downloads

    schedules = [] #schedules are put in a list

    for x in downloads:
        schedule = Schedule.query.filter_by(scheduleId = x.scheduleId).first() #for every element in downloads, checks if existing scheduleId for sched id in download entry

        if schedule:
            schedules.append(schedule) # if so, add

    return render_template('downloads.html', schedules = schedules)

@sched.route('/downloadschedule/<int:schedId>')
@login_required
def downloadSchedule(schedId):

    uId = current_user.get_id()

    check = Schedule.query.filter_by(scheduleId = schedId).first() #check if the schedule actually exists
    alreadyExists = Download.query.filter_by(scheduleId = schedId, userId = uId).first() #check if download already exists

    if not check or alreadyExists:
        redirect(url_for('sched.schedules'))

    new = Download(check.scheduleId, uId)
    db.session.add(new)
    db.session.commit()

    schedules = Schedule.query.order_by(Schedule.scheduleId).all()
    return redirect(url_for('sched.getDownloads'))

@sched.route('/schedules/<int:schedId>/remove')
@login_required
def deleteSchedule(schedId):

    uId = current_user.get_id()
    user = User.query.filter_by(id = uId).first()
    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    if not sched or sched.creatorId != uId or not user.isAdmin:
        redirect(url_for('sched.schedules'))

    events = Event.query.filter_by(scheduleId = schedId).all()

    for event in events:
        db.session.delete(event)

    downloads = Download.query.filter_by(scheduleId = schedId).all()

    for download in downloads:
        db.session.delete(download)

    db.session.delete(sched)
    db.session.commit()

    return redirect(url_for('sched.schedules'))


@sched.route('/schedules/<int:schedId>/edit')
@login_required
def editSchedule(schedId):

    uId = current_user.get_id()
    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    if not sched or sched.creatorId != uId:
        redirect(url_for('sched.schedules'))

    return render_template('editschedule.html', sched = sched)



@sched.route('/schedules/<int:schedId>/edit', methods = ['POST'])
@login_required
def saveScheduleChanges(schedId):

    sched = Schedule.query.filter_by(scheduleId = schedId).first()

    name = request.form.get('name')
    start = request.form.get('sDate')
    end = request.form.get('eDate')

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
        return render_template('editschedule.html', sched = sched)
    
    events = Event.query.filter_by(scheduleId = schedId).all()

    #check if events are still in timeframe of schedule
    for event in events:

        eStart = event.startTime.timestamp()
        eEnd = event.endTime.timestamp()

        if (eStart < startSeconds) or (eEnd > endSeconds):
            flash('is not in range of event in schedule!')
            return render_template('editschedule.html', sched = sched)


    sched.scheduleName = name
    sched.startDate = startD
    sched.endDate = endD

    db.session.commit()

    return redirect(url_for('sched.schedules'))
