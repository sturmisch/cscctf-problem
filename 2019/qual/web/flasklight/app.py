from flask import Flask, request, render_template_string, abort

app = Flask(__name__)
app.secret_key = 'CCC{f4k3_Fl49_:v} CCC{the_flag_is_this_dir}'
result = ["CCC{Fl49_p@l5u}", "CSC CTF 2019", "Welcome to CTF Bois", "CCC{Qmu_T3rtyPuuuuuu}", "Tralala_trilili"]
@app.route("/")
def search():
  global result
  blacklist = ['url_for', 'listdir', 'globals']
  search = request.args.get('search') or None
  if search is not None:
    for black in blacklist:
      if black in search:
        abort(500)
  if search in result:
    result = search
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
  <title>Flasklight</title>
</head>
<body>
  <marquee><h1>Flasklight</h1></marquee>
  <h2>You searched for:</h2>
  <h3>%s</h3>
  <br>
  <h2>Here is your result</h2>
  <h3>%s</h3>
</body>
</html>''' % (search, result))
  elif search == None:
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
  <title>Flasklight</title>
</head>
<body>
  <marquee><h1>Flasklight</h1></marquee>
  <h2>You searched for:</h2>
  <h3>%s</h3>
  <br>
  <h2>Here is your result</h2>
  <h3>%s</h3><br>
  <!-- Parameter Name: search -->
  <!-- Method: GET -->
</body>
</html>''' % (search, result))
  else:
    result = []
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
  <title>Flasklight</title>
</head>
<body>
  <marquee><h1>Flasklight</h1></marquee>
  <h2>You searched for:</h2>
  <h3>%s</h3>
  <br>
  <h2>Here is your result</h2>
  <h3>%s</h3>
</body>
</html>''' % (search, result))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=9000)
