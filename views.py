__author__ = 'deekras'

from flask import Flask, render_template, redirect, request
from os import urandom

from models import personality_traits

app = Flask(__name__)
WTF_CSRF_ENABLED = True
SECRET_KEY = urandom(32)

app.secret_key = urandom(32)

@app.route("/traits", methods = ['GET', 'POST'])
def traits():
    if request.method == 'POST':
        submitted_mode = request.form['mode']
        submitted_traits = request.form.getlist('trait')
        print submitted_traits
        update_traits(submitted_mode, submitted_traits)
    other_traits, traits_have, traits_unhappy, traits_wish = categorize_traits()
    return render_template('traits.html', other_traits=other_traits,
                                                 traits_have=traits_have,
                                                 traits_unhappy=traits_unhappy,
                                                 traits_wish=traits_wish)

def update_traits(submitted_mode, submitted_traits):
   for trait in submitted_traits:
       if submitted_mode == "traits I have":
          personality_traits[unicode(trait)] = 1
       elif submitted_mode == "traits I have that I don't like":
          personality_traits[str(trait)] = 2
       elif submitted_mode == "traits I wish I had":
          personality_traits[str(trait)] = 3
       elif submitted_mode == "oops, mark as unmarked":
          personality_traits[str(trait)] = 0


def categorize_traits():
    other_traits = []
    traits_have = []
    traits_unhappy = []
    traits_wish = []
    for trait in personality_traits:
        if personality_traits[trait] == 0:
            other_traits.append(trait)
        elif personality_traits[trait] == 1:
            traits_have.append(trait)
        elif personality_traits[trait] == 2:
            traits_unhappy.append(trait)
        elif personality_traits[trait] == 3:
            traits_wish.append(trait)
    return other_traits, traits_have, traits_unhappy, traits_wish



if __name__ == '__main__':
    app.run(debug=True)