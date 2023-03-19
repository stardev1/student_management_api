from api.v1 import create_app

app = create_app( True)

@app.route('/')
def hello_world():
    return 'Student management system API. please go to /api for swagger ui'



if __name__ == '__main__':
    app.run(debug=True)