from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugtoolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"
app = FLask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

degug = DebugtoolbarExtension(app)

@app.route("/")
# the homepage with the base html where we start our survey
def survey_start():
    """Select Survey."""
    return render_template("survey_start.html", survey = survey)

@app.route('/begin', methods=["POST"])
def start_survey():
    """begins the survey"""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")
    #sends them to the first questions and makes an empty response which will be filled as they go.

@app.route('/questions<int:qid>')
# we created a route designed for filling out multiple surveys.
# Create a function that will add answers from the question form to our response variable
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)
# lets add some conditional logic to ensure the user interacts the way we want.
    if (responses is None):
        return redirect("/")

    if(len(responses) == len(survey.questions)): #if they filled it out correctly based from the questions  within the survey
        return redirect("/complete")

    if (len(responses) != qid):
        #trying to access questions out of order.
        flash(f"invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num = qid, question = question)

@app.route('/answer', methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    #get response from the choices
    choice = request.form['answer']
    
    #we need to add this into our session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    #add a logic to check if the user has given all the answers to the questions provided
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    else:
        return redirect(f"/questions/{len(responses)}")
    #if the logic isnt met when submitted, return them to the questions. if it is, sends them to the completed page

@app.route('/complete')
def complete():
    """when survey is done, show completion page."""
    return render_template('completion.html')