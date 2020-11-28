from flask import Blueprint, render_template, session, redirect, url_for
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
    if len(hat.names) == 0:
        return render_template('draw-name.html', name=None, name_count=len(hat.names))

    # user has already drawn a name
    if 'name' in session:
        return render_template('draw-name.html', name=session['name'], name_count=len(hat.names))

    name = random.choice(hat.names)
    session['name'] = name.name

    db.session.delete(name)
    db.session.commit()

    hat = Hat.query.filter_by(hat_number=hat_number).first()
    return render_template('draw-name.html', name=session['name'], name_count=len(hat.names))
