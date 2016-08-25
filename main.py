
import webapp2
import re
import cgi

error_username = ""
error_password = ""
error_verify = ""
error_email = ""
user_name = ""
user_email = ""

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>SignUp</title>
    <style type="text/css">

        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Sign Up</a>
    </h1>
"""



signup_form = """
        <form method="post">
        <table>
        <tr>
            <td><label for="username">Username</label></td>
            <td><input type="text" name="username" value="%s"><span class="error">%s<span></td>
        </tr>
        <tr>
            <td><label for="password">Password</label></td>
            <td><input type="password" name="password"/><span class="error">%s</span></td>
        </tr>
        <tr>
            <td><label for="verify">Verify Password</label></td>
            <td><input type="password" name="verify"/><span class="error">%s</span><td>
        </tr>
        <tr>
            <td><label for="email">Email Address (optional)</label></td>
            <td><input type="text" name="email"value=%s><span class="error">%s</span></td>
        </tr>
        </table>
        <input type="submit"/>
        </form>
    """ % (user_name,  error_username, error_password, error_verify, user_email, error_email)

page_footer = """
    </body>
    </html>
    """

class Index(webapp2.RequestHandler):

    def get(self):
        response = page_header + signup_form + page_footer
        self.response.write(response)

    def post(self):
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        user_name = ""
        user_email = ""

        def valid_password(password):
            return PASSWORD_RE.match(password)

        def valid_username(username):
            return USER_RE.match(username)

        def valid_email(email):
            return EMAIL_RE.match(email)

        user_name = self.request.get(cgi.escape("username", quote=True))
        user_email = self.request.get("email")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        validEmail = valid_email(user_email)


        if user_password == user_verify:
            valid = True
        else:
            error_verify = "That is not the same as the password you entered"
            valid = False

        if not valid_username(user_name):
            error_username = user_name + " is not a valid user name."

        if not valid_password(user_password):
            error_password = "That was not a valid password."

        if user_email == "":
            validEmail = True
        elif not validEmail:
                error_email = "This is not a valid email."

        if valid_username(user_name) and valid_password(user_password) and validEmail and valid:
            self.redirect("/welcome?username={}".format(user_name))

        signup_form = """
                <form method="post">
                <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td><input type="text" name="username" value="%s"><span class="error">%s<span></td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td><input type="password" name="password"/><span class="error">%s</span></td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td><input type="password" name="verify"/><span class="error">%s</span><td>
                </tr>
                <tr>
                    <td><label for="email">Email Address (optional)</label></td>
                    <td><input type="text" name="email"value=%s><span class="error">%s</span></td>
                </tr>
                </table>
                <input type="submit"/>
                </form>
            """ % (user_name,  error_username, error_password, error_verify, user_email, error_email)

        response1 = page_header + signup_form + page_footer
        self.response.write(response1)

class Welcome(webapp2.RequestHandler):
    def get(self):

        welcome_form = """
        <p><h1>Welcome!</h1></p>
        <p>Your sign up is complete, {}. Welcome!</p>
        """.format(self.request.get("username"))

        response = page_header + welcome_form + page_footer
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
