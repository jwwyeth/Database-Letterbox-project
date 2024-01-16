import sqlite3
import os 
import subprocess

 
def user_login(con,cur):
   flag=True
   while(flag):
      print("1. Login\n2. Create New Account")
      answer=input()
      if(answer=="Login"):
        Username=input("Username:")
        Password=input("Password:")
        cur.execute( "SELECT COUNT(*) FROM User WHERE (username= ? AND password = ?)",(Username,Password))
        verification=cur.fetchone()
        print(verification)
   #if we find a match then we can return true and login
        if (verification[0]>0):
          flag=False
          print("Welcome ",Username)
          #return username for use later
          return Username
        else:
          clear_console()
          print("Login failed to verify or User not found, Please try again")
      if(answer=="Create New Account"):
        # need to probe for same username potentiallity
        new_Username=input("New Username:")
        new_Password=input("New Password:")
        try:
        #try to add new account
          cur.execute("INSERT INTO User (username, password) VALUES (?,?)", (new_Username, new_Password))
          con.commit( )
          clear_console()        #except if it already exists
        except sqlite3.IntegrityError:
          clear_console()
          print("Username ",new_Username," already exists, new account failed to be created")
      else:
        clear_console()
        print("Invalid Input")


#this function deletes a user
def delete_user(con, cur,current_user):
  delete_statement=("DELETE FROM User WHERE username=?")
  cur.execute(delete_statement,(current_user,))
  clear_console()
  print("Account deleted, Sorry to see you go :(")
  con.commit()
  return 
  

#used to display user table
def show_user_table(cur):
  cur.execute("SELECT * FROM User")
  print(cur.fetchall())
  return

def show_movie_table(cur):
  clear_console()
  flag=True
  while(flag):
    cur.execute("""SELECT title, genre, round(avg_rating,2) FROM Movie""")
    rows = cur.fetchall()
    print("Title".ljust(20) + "|" + "Genre".ljust(20) + "|" + "Average Rating")
    print("-" * 60)
    for row in rows:
            print(f"{row[0].ljust(20)} | {row[1].ljust(20)} | {row[2]:.2f}")
            print("-" * 60)
    User_choice=input("Type 'return' to go back to the main menu, 'view:(movie title)' to view a movie in greater detail, \nor '(movie title):reviews' to see reviews for a certain movie .\n")
    
    User_choice=User_choice.split(":")
    if (User_choice[0]=="return"):
      flag=False
      clear_console()
      return
    if(User_choice[0]=="view"):
      #we check to if movie exists
      cur.execute("SELECT COUNT(*) FROM Movie WHERE title=?", (User_choice[1],))
      count = cur.fetchone()[0]
  #Movie doesn't exists in database
      if(count==0):
        clear_console()
        print("That movie does not exists in our database, sorry.\n")
  #Movie exists in database
      if(count>0):   
        in_depth_display( cur,User_choice[1])

    if(User_choice[1]=="reviews" ):
      #this clause will show all reviews for movie given 
      #we check to if movie exists
      cur.execute("SELECT COUNT(*) FROM Movie WHERE title=?", (User_choice[0],))
      count = cur.fetchone()[0]
  #Movie doesn't exists in database
      if(count==0):
        clear_console()
        print("That movie does not exists in our database, sorry.\n")
  #Movie exists in database
      if(count>0):   
        show_review_table( cur,User_choice[0])

    else:
      clear_console()
      print("Invalid input\n")    
  return

def show_review_table(cur,film_title):
  clear_console()
  stopper=True
  cur.execute("""SELECT user, rating, review FROM rate_review WHERE title=?""",(film_title,))
  rows=cur.fetchall()
  for row in rows:
    user, rating, review=row
    print(user)
    print(rating," out of 5 stars")
    print(review)
    print("---------------------------------------------------")
  while (stopper):
    return_command=input("Type return if you wish to return to the movie library\n")
    if(return_command=="return"):
       clear_console()
       stopper=False
    else:
       
       print("Invalid input")

  return


def insert_movie_command(cur,conn):
  clear_console()
  print("For the insertion please give the film's title, its genre, and a short synopsis of the film's plot in the given order.\n")

  title=input()
  Genre=input()
  synopsis=input()
  cur.execute("SELECT COUNT(*) FROM Movie WHERE (title=?)", (title,))
  first_time_checker=cur.fetchone()[0]
  if(first_time_checker!=0):
      clear_console()
      print("Sorry that film already exists in our database.\n")
  else:

    command = 'INSERT INTO Movie (title, genre, Movie_Synopsis) VALUES (?,?,?)'
    cur = conn.cursor()
    cur.execute(command, (title, Genre, synopsis))
    conn.commit()
  return

def insert_crew_command(cur,conn):
  clear_console()
  print("For the insertion please give the name of the person, their profession (being Actor, Director, or Producer), and the film they worked on in the given order.\n")
  name=input()
  profession=input()
  title=input()
  
  clear_console()
  if(profession=='Actor' or profession=='Director' or profession=='Producer'):
    cur.execute("SELECT COUNT(*) FROM People WHERE (name=? AND profession=? AND title=?)", (name, profession, title))
    first_time_checker=cur.fetchone()[0]
    if(first_time_checker!=0):
      clear_console()
      print("Sorry that crew member already exists in our database.\n")
    else:
      command = 'INSERT INTO People (name, profession, title) VALUES (?,?,?)'
      cur = conn.cursor()
      cur.execute(command, (name, profession, title))
      conn.commit()
      cur.execute("SELECT * FROM People")
      print(cur.fetchall())

  else:
    clear_console()
    print("Invalid input\n")
    return
    
  return



def rate_review(conn,cur,username):
#please type the film you want to review
  clear_console()
  film_title=input("Which movie would you like to leave a review for?\n")

  cur.execute("SELECT COUNT(*) FROM Movie WHERE title=?", (film_title,))
  count = cur.fetchone()[0]

  #Movie doesn't exists in database
  if(count==0):
    clear_console()
    print("That movie does not exists in our database, sorry.")
    return
  #Movie exists in database
  if(count>0):
    #verify that this is the users only comment
    cur.execute("SELECT COUNT(*) FROM rate_review WHERE (title=? AND user=?)", (film_title, username))
    first_time_checker=cur.fetchone()[0]
    if(first_time_checker!=0):
      clear_console()
      print("Sorry you already gave a review for this film.")

    else:
      rating=int(input("Out of a score of 5 stars what would you rate the film?\n"))
      if(rating>0 and rating<=5):
        flag=False
      #user asks outside of the boundary
      else:
        clear_console()
        print("Sorry that was not a valid number given")
        return 

      review=input("Please input a short statement about your opinions on the film.\n")
      insertion_command="INSERT INTO rate_review VALUES (?,?,?,?)"
      cur.execute(insertion_command,(username,film_title,review,rating))

    # at this point the table should have been updated with the new review and thus we now need to change the avg rating in movie tabel
    
      take_average(cur,conn,film_title)
      conn.commit()
      clear_console()
      return

def in_depth_display(cur,film_title):
  clear_console()
  stopper=True
  while (stopper):
     cur.execute("""SELECT title, genre, round(avg_rating,2), Movie_synopsis FROM Movie WHERE title=?""",(film_title,))
     # we need to disaply the film information, and the snyopsis should fall below the intial three values and have actors listed in between
     print("Title".ljust(20) + "|" + "Genre".ljust(20) + "|" + "Average Rating")
     print("-" * 60)

     results = cur.fetchall()

     movie = results[0]
     print(f"{movie[0].ljust(20)} | {movie[1].ljust(20)} | {movie[2]:.2f}")   

     cur.execute("""SELECT name, profession FROM People WHERE title=?""",(film_title,))
     people = cur.fetchall()
     print("\nPeople involved:\n-----------------")
     for person in people:
        print(f"{person[0]} ({person[1]})")      
     #THIS IS LIKE ONE OF THE LAST THINGS WE NEED I JUST GOT REALLLY BRAIN DEAD AT THE MOMENT
     #NEED TO LIST ALL PEOPLE THAT WORKED ON MOVIE RIGHT HERE
     
     
    
     print("\nMovie Synopsis:")
     print(movie[3],"\n")
     return_command=input("Type return if you wish to return to the movie library\n")
     if(return_command=="return"):
       stopper=False
       clear_console()
     else:
       clear_console()
       print("Invalid input")

  return

#user gives a rating and little blurb
#then fill in inputs and movie into table
#
#view others review in the library view tab?
   

def take_average(cur, conn,film):
    averge_num = "SELECT AVG(rating) FROM rate_review WHERE title = ?"
    apply_average = "UPDATE Movie SET avg_rating = ? WHERE title = ?"     
    
    cur.execute(averge_num, (film,))
    avg_rating=cur.fetchone()[0]
    cur.execute(apply_average, (avg_rating, film))
    conn.commit()
    
    return
    # use the .schema command to view the schema of the rate_review table
def search(cur,con):
   clear_console()
   category=input("What category would you like to search based on?\n")
   search_term=input("Insert your search term below:\n")
   clear_console()
   if(category=="Genre"):
      cur.execute("""SELECT title, genre, round(avg_rating,2) FROM Movie WHERE genre=?""",(search_term,))
      rows = cur.fetchall()
      print("Title".ljust(20) + "|" + "Genre".ljust(20) + "|" + "Average Rating")
      print("-" * 60)
      for row in rows:
            print(f"{row[0].ljust(20)} | {row[1].ljust(20)} | {row[2]:.2f}")
            print("-" * 60)
   if(category=="Title"):
     cur.execute("""SELECT title, genre, round(avg_rating,2) FROM Movie WHERE title=?""",(search_term,))
     rows = cur.fetchall()
     print("Title".ljust(20) + "|" + "Genre".ljust(20) + "|" + "Average Rating")
     print("-" * 60)
     for row in rows:
            print(f"{row[0].ljust(20)} | {row[1].ljust(20)} | {row[2]:.2f}")
            print("-" * 60)
   if(category=="Person"):
      cur.execute("""SELECT name, profession, title FROM People WHERE name=?""",(search_term,))
      rows = cur.fetchall()
      print("Name".ljust(20) + "|" + "Profession".ljust(20) + "|" + "Worked on")
      print("-" * 60)
      for row in rows:
        print(f"{row[0].ljust(20)} | {row[1].ljust(20)} | {row[2].ljust(20)}")
        print("-" * 60)
   stopper=True
   while (stopper):
    return_command=input("Type return if you wish to return to the movie library\n")
    if(return_command=="return"):
       clear_console()
       stopper=False
    else:
       
       print("Invalid input")

  
   return 

def execute_sql_file(cur, filename):
    with open(filename, 'r') as file:
       cur.executescript(file.read())
    return


def clear_console():
    if os.name == 'nt': # If the operating system is Windows
        os.system('cls')
    else: # If the operating system is Linux or MacOS
        os.system('clear')


def movie_presentation(cur, conn):
    clear_console()
    while(True):
      print()
      print("1.Add film files\n2.Watch Movie\n3.View current movie selection\n4.Delete Movie file \n5.return")

      print("\n Pleas type out any of the commands listed to use the database:\n")

      user_input=input()

      if(user_input == "Add film files"):
        print("please enter the movie name")
        name_input = input()
        cur.execute("SELECT COUNT(*) FROM files WHERE (movie_name=?)", (name_input,))
        first_time_checker=cur.fetchone()[0]
        if(first_time_checker!=0):
          print("Sorry that files already exists in our database.\n")
          break

        
        print("Please enter the exact files path to the movie")
        file_input = input()
        

        command = 'INSERT INTO files (movie_name, file) VALUES (?,?)'
        cur = conn.cursor()
        cur.execute(command, (name_input, file_input))
        conn.commit()
        clear_console()


      if(user_input == "Watch Movie"):
        clear_console()
        print("please enter the name of the film you would like to watch")
        movie_input = input()
        cur.execute("SELECT COUNT(*) FROM files WHERE (movie_name=?)", (movie_input,))
        first_time_checker=cur.fetchone()[0]
        if(first_time_checker==0):
          print("This movie is not in the file table\n")
        else:
            cur.execute("""SELECT file FROM files WHERE movie_name=?""",(movie_input,))
            temp = cur.fetchall()[0]
            process = subprocess.Popen(temp, shell=True)
            clear_console()
            
      if(user_input == "View current movie selection"):
        clear_console()
        cur.execute("""SELECT movie_name,file FROM files""")
        rows=cur.fetchall()

        for row in rows:
          print(f"Title: {row[0].ljust(20)}|Path: {row[1].ljust(20)}")       
          print("-" * 60)
     
      


      if(user_input == "Delete Movie file"):
        clear_console()
        print("please enter the name of the movie you would like to delete")
        delete_movie_input = input()
        delete_statement=("DELETE FROM files WHERE movie_name=?")
        cur.execute(delete_statement,(delete_movie_input,))
        conn.commit()
        clear_console()
        print(delete_movie_input, " was deleted\n")

      if(user_input == "return"):
          clear_console()
          return
      
    return

       
def main():
  #need to make a table that stores users and password
  #need to create a function that will add new tuples to this list if they want to be a new user 
  con = sqlite3.connect("MovieDataBase.db")
  cur = con.cursor()
  execute_sql_file(cur, 'Movie_database.sql')
  flag=True
  
  #at this point we have created a table for movies and users
  #if the user logs in succesffuly we carry on with the operatins 
  #we assign the return value to current_user as to have means to call upon who is currently logged in
  current_user=user_login(con,cur)
  #print(current_user)

  #this command enables our output to not be a string of outputs but clears our table so to speak
  clear_console()
  while (flag):
    print("Welcome ",current_user)
    print("1.View Library\n2.Search\n3.Add Film\n4.Add Crew Member\n5.Rate and Review\n6.View Watchable Films\n7.Delete Account\n8.Log Out\n")
    print("\n Pleas type out any of the commands listed to use the database:\n")
    user_input=input()

    if user_input =="View Library":
     show_movie_table(cur)

    if user_input=="Search":
      search(cur,con)
    if user_input=="Add Film":
      insert_movie_command(cur,con)

    if user_input=="Add Crew Member":
      insert_crew_command(cur,con)

    if user_input=="Rate and Review":
      rate_review(con,cur,current_user)
    
    if user_input=="Delete Account":
      delete_user(con,cur,current_user)
      #find new account to log into 
      current_user=user_login(con, cur)
    if user_input=="View Watchable Films":
     movie_presentation(cur,con)
     

     
    if user_input=="Log Out":
      
      clear_console()
      current_user=user_login(con, cur)


    else:
      clear_console()


       

  con.close()

if __name__=="__main__": 
    main() 





