from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

import os

from MorseConvert.convert import english_to_morse, morse_to_english


class MorseForm(FlaskForm):
    english = StringField("English")
    morse_code = StringField("Morse Code")
    submit = SubmitField("Convert")
    reset = SubmitField("Reset")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
bootstrap = Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def convert():
    morse_form = MorseForm()
    if morse_form.validate_on_submit():
        if morse_form.submit.data:
            eng_fill = morse_to_english(morse_form.morse_code.data)
            if eng_fill == "":
                morse_form.english.data = morse_form.english.data
            else:
                morse_form.english.data = eng_fill
            mor_fill = english_to_morse(morse_form.english.data)
            if mor_fill == "":
                morse_form.morse_code.data = morse_form.morse_code.data
            else:
                morse_form.morse_code.data = mor_fill
            return render_template('convert.html', form=morse_form)
        else:
            return redirect(url_for("convert"))
    return render_template('convert.html', form=morse_form)


if __name__ == "__main__":
    app.run(debug=True)