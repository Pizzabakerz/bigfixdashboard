from flask import Flask,jsonify,request,make_response
import jwt
import datetime
from functools import wraps

# app config
app = Flask(__name__)
app.config['SECRET_KEY'] = "INkl9f342rubfbqwjbuiIJGL"

# Auth token
def token_req(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        # example
        # http:localhost:5000/route?token=afjfadbjsometoken
        token = request.args.get('token') 

        if not token:
            return jsonify({'message': " Token Is Missing "}),403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        
        except Exception as e:
            return jsonify({'message': " Token Is Invalid "}),403
        return f(*args,**kwargs)
    return decorated
    
# route begins
@app.route('/')
@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == "password":
        token = jwt.encode({'user':auth.username,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)},app.config['SECRET_KEY'])
        return jsonify({'auth':"sucess",'token':token.decode('UTF-8'),'status':200})
    return make_response('could not verify',401,{'WWW-Authenticate':'basic realm = "Login Required" '})

# sample protected api
@app.route('/api/v1/protected')
@token_req
def sample_protected():
    return jsonify({'message':"this is a protected data"})

# sample unprotected api
@app.route('/api/v1/unprotected')
def sample_unprotected():
    return jsonify({'message':"this is an unprotected data"})

if __name__ == "__main__":
    app.run(debug=True)