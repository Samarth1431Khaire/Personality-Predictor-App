from flask import Flask, render_template, request, url_for, redirect, session
from sqlite3 import*

import pickle
app=Flask(__name__)
app.secret_key="personality prediction"



@app.route("/", methods=["GET","POST"])

def home():
  if "un" in session:
        
      if request.method=="POST":
         if request.form['action']=="Find":
                 f=None
                 model=None
                 try:
                      f=open("pp.model", "rb")
                      model=pickle.load(f)
                 except Exception as e:
                       msg="f issue" + str(e)
                       return render_template("home.html", msg=msg)
                 finally:
                       if f is not None:
                               f.close()
                 if model is not None:
                       ag=float(request.form["ag"])
                       o=float(request.form["o"])
                       n=float(request.form["n"])
                       c=float(request.form["c"])
                       a=float(request.form["a"])
                       e=float(request.form["e"])
                       data=[ag, o, n, c, a, e]
             	       

                       g=float(request.form["g"])
                       if g==1:
                           data.extend([1,0])
                       else:
                           data.extend([0,1])

                       ans=model.predict([data])
                       if ans[0]=="extraverted":
                               msg=" Your Personality is:Extraverted\n\n"+"You Should listen Following songs:-\n"+"1. Only Time\n"+"2. Chahun Main Ya Na\n"+"3. Tum Ho\n"+"4. Saajna Unplugged\n"+"5. Rehna Tu"
                       elif ans[0]=="serious":
                               msg=" Your Personality is:Serious\n\n"+"You Should listen Following songs:-\n"+"1. The Bussiness\n"+"2. Bananza\n"+"3. Dance Monkey\n"+"4. Freed from Desire\n"+"5. Gimme Gimme Gimme"
                       elif ans[0]=="responsible":
                               msg=" Your Personality is:Responsible\n\n"+"You Should listen Following songs:-\n"+"1. Dil KO Karaar\n"+"2. Ranjha\n"+"3. Tu Aake Dekhle\n"+"4. Aashiqui Aa Gayi\n"+"5. Agar Tum Saath Ho"
                       elif ans[0]=="lively":
                               msg=" Your Personality is:Lively\n\n"+"You Should listen Following songs:-\n"+"1. Good Times\n"+"2. The Best\n"+"3. Respect\n"+"4. Spinning Around\n"+"5. We Are Family"
                       else:
                              msg=" Your Personality is:Dependable\n\n"+"You Should listen Following songs:-\n"+"1. Eye of the Tiger\n"+"2. Stronger\n"+"3. Lose Yourself\n"+"4. Walking on Sunshine\n"+"5. Remember the Name" 
                               
                              
                
                
                
                
                       return redirect(url_for('music', msg=msg))
                 else:
                       return render_template("home.html", msg="model issue")
         elif request.form['action']=="Logout":
                  session.pop('un', None)
                  return redirect(url_for('login'))
                  
         else:
                  return render_template("home.html")
                  
                  
      else:
               return render_template("home.html")
  else:
          return redirect(url_for('login'))


@app.route("/music", methods=["GET","POST"])
def music():
      msg=request.args.get('msg', None)
      return render_template("music.html", msg=msg)
      
             

@app.route("/signup",methods=["GET","POST"])
def signup():
      if "un" in session:
             return redirect(url_for('home'))
      
      if request.method=="POST":
               un=request.form["un"]
               pw1=request.form["pw1"] 
               pw2=request.form["pw2"]
               if pw1==pw2:
                      con=None
                      try:
                           con=connect("pp.db")
                           cursor=con.cursor()
                           sql="insert into users values('%s','%s')"
                           cursor.execute(sql%(un,pw1))
                           con.commit()
                           return redirect(url_for('login'))

                      except Exception as e:
                             con.rollback()
                             return render_template("signup.html", msg="user already exits" + str(e))
                      finally:
                              if con is not None:
                                      con.close()
               else:
                    return render_template("signup.html", msg="passwords did not match")

      else:
             return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
       if "un" in session:
             return redirect(url_for('home'))
      
       if request.method=="POST":
               un=request.form["un"]
               pw=request.form["pw"] 
               con=None
               try:
                        con=connect("pp.db")
                        cursor=con.cursor()
                        sql="select * from users where username='%s' and password='%s'"

                        cursor.execute(sql % (un,pw))
                        data=cursor.fetchall()
                        if len(data)==0:
                              return render_template("login.html", msg="invalid login")
                        else:
                             session["un"]=un
                             return redirect(url_for('home'))
               except Exception as e:
                           return render_template("login.html", msg=str(e))
               finally:
                          if con is not None:
                              con.close()
       else:
               return render_template("login.html")

@app.route("/readme", methods=["GET","POST"])
def readme():
        if "un" in session:
             return redirect(url_for('home'))

        return render_template("readme.html")

@app.route("/about", methods=["GET","POST"])
def about():
        if "un" in session:
             return render_template("about.html") 


@app.route("/contact", methods=["GET","POST"])
def contact():
        if "un" in session:
             return render_template("contact.html") 


@app.route("/care", methods=["GET","POST"])
def care():
        if "un" in session:
             return render_template("care.html") 

     
  
     

@app.errorhandler(404)
def not_found(e):
        return redirect(url_for('login'))



if __name__=="__main__":
        app.run(debug=True, use_reloader=True)