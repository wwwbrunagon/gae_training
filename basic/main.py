# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2

form="""
<form method="post">
    What is your birthday?
    <br>
    <br>
    <label>Month <input type="text" name="month" value="%(month)s"></label>
    <label>Day <input type="text" name="day" value="%(day)s"></label>
    <label>Year <input type="text" name="year" value="%(year)s"></label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(),m) for m in months)

class MainPage(webapp2.RequestHandler):
    def valid_month(self, month):
        if month:
            short_month = month[:3].lower()
            return month_abbvs.get(short_month)

    def valid_day(self, day):
        if day and day.isdigit():
            day = int(day)
            if day > 0 and day <= 31:
                return day

    def valid_year(self, year):
        if year and  year.isdigit():
            year = int(year)
            if year > 1900 and year <= 2020:
                return year

    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": month,
                                        "day": day,
                                        "year": year})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = self.valid_month(user_month)
        day = self.valid_day(user_day)
        year = self.valid_year(user_year)

        if not (month and day and year):
            self.write_form("That's doesn't look valid to me, friend",
                            user_month, user_day, user_year)
        else:
            self.redirect("/thanks")


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([('/', MainPage),('/thanks',ThanksHandler)],
                              debug=True)





