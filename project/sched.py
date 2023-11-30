from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import User, Schedule
import datetime


sched = Blueprint('sched', __name__)

@sched.route('/schedules')
def schedules():
    return 'nuts'

@sched.route('/events')
def events():
    return 'deez'

@sched.route('/createschedule')
def createSched():
    return render_template('createschedule.html')

@sched.route('/schedules', methods = ['POST'])
def insertSched():

    name = request.form.get('name')
    startD = request.form.get('sDate')
    endD = request.form.get('endD')

    if (startD.now() - endD.now()) > 0:
        flash('Time wrong')
        return redirect(url_for('sched.createSched'))
    
    if not name:
        flash ('no name')
        return redirect(url_for('sched.createSched'))

    new = Schedule()

    db.session.add(new)
    db.session.commit()

    return redirect(url_for('sched.schedules'))