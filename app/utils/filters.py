# Jinja Filters

#This function expects a "datetime" object and uses the "strftime()" method to convert it
#to a string using the defined format.
def format_date(date):
  return date.strftime('%m/%d/%y')


#Format the URLs so that only the "domain" remains
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]


#Handle the pluralization of certain words, based on the count passed in
def format_plural(count, word):
  if count != 1:
    return word + 's'

  return word


# Testing code
# from datetime import datetime
# print(format_date(datetime.now()))

# print(format_url('http://google.com/test/'))
# print(format_url('https://www.google.com?q=test'))

# print(format_plural(2, 'cat'))
# print(format_plural(1, 'dog'))