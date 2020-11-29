from flask import Blueprint, render_template, session, redirect, url_for, flash
import random
import strgen
from .forms import EnterExisting, AddName
from .models.hat import Hat
from .models.name import Name
from . import db

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
def index_controller():
    enter_existing_form = EnterExisting()

    if enter_existing_form.validate_on_submit():
        return redirect(url_for('main.draw_name_controller', hat_number=enter_existing_form.hat_number.data))

    return render_template('index.html', enter_existing_form=enter_existing_form)


@main_blueprint.route('/new')
def new_controller():
    hat = Hat()
    hat.hat_number = strgen.StringGenerator("[A-Z]{8}").render()
    db.session.add(hat)
    db.session.commit()
    return render_template('new.html', hat=hat)


@main_blueprint.route('/add-name/<hat_number>', methods=['GET', 'POST'])
def add_name_controller(hat_number):
    hat = Hat.query.filter_by(hat_number=hat_number).first()
    form = AddName()
    if form.validate_on_submit():
        name = Name()
        name.hat_id = hat.id
        name.name = form.name.data

        flip = random.randrange(0, 2)
        if flip == 1:
            name.disposition = 'Naughty'
        else:
            name.disposition = 'Nice'

        db.session.add(name)
        db.session.commit()

        hat = Hat.query.filter_by(hat_number=hat_number).first()
        return render_template('add-name.html', hat=hat, form=form, name_count=len(hat.names))

    return render_template('add-name.html', hat=hat, form=form, name_count=len(hat.names))


@main_blueprint.route('/draw-name/<hat_number>')
def draw_name_controller(hat_number):
    hat = Hat.query.filter_by(hat_number=hat_number).first()

    if hat is None:
        flash("Sorry, we couldn't find the hat you are looking for")
        return redirect(url_for('main.index_controller'))

    if len(hat.names) == 0:
        return render_template('draw-name.html', name=None, name_count=len(hat.names), hat=hat)

    # user has already drawn a name
    if hat.hat_number in session:
        return render_template('draw-name.html', name=session[hat.hat_number], name_count=len(hat.names), hat=hat)

    name = random.choice(hat.names)
    session[hat.hat_number] = name.name

    db.session.delete(name)
    db.session.commit()

    hat = Hat.query.filter_by(hat_number=hat_number).first()
    return render_template('draw-name.html', name=session[hat.hat_number], name_count=len(hat.names), hat=hat)


@main_blueprint.route('/redraw/<hat_number>')
def redraw_controller(hat_number):
    hat = Hat.query.filter_by(hat_number=hat_number).first()

    if len(hat.names) == 0:
        flash('There are no more names to redraw')
        return redirect(url_for('main.index_controller'))

    # draw a new name which is different
    name = random.choice(hat.names)
    new_name = name.name
    db.session.delete(name)

    # add the old name back to the hat
    old_name = Name()
    old_name.name = session[hat.hat_number]
    old_name.hat_id = hat.id
    old_name.disposition = 'Naughty'
    db.session.add(old_name)

    # commit the change
    db.session.commit()

    # update the users draw
    session[hat.hat_number] = new_name

    return render_template('draw-name.html', name=session[hat.hat_number], name_count=len(hat.names), hat=hat)
