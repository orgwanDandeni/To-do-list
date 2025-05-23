from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client

SUPABASE_URL = ""
SUPABASE_KEY = ""

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = Flask(__name__)

@app.route('/')
def index():
    response = supabase.table('tasks').select("*").order('created_at', desc=True).execute()
    tasks = response.data
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    supabase.table('tasks').insert({'title': title, 'completed': False}).execute()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    task = supabase.table('tasks').select("*").eq('id', id).execute().data[0]
    supabase.table('tasks').update({'completed': not task['completed']}).eq('id', id).execute()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    supabase.table('tasks').delete().eq('id', id).execute()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
