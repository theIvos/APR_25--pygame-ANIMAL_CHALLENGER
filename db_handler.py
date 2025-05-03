import mysql.connector
from random import randint

def handle_db(action, parm1 = "", parm2 = "", parm3 = "", parm4 = "", parm5 = "", parm6 ="", parm7="",parm8="",parm9="",parm10="",parm11="",parm12=""):
    try:
        mydb = mysql.connector.connect(
            host = "mysql-animalchallenger.alwaysdata.net",
            user = "410741", 
            password = "na3aruuALWAYSDATA",  
            port = 3306,
            database = "animalchallenger_main" 
        )

    except mysql.connector.Error as err:
        print(f"Chyba pri pripojovani: {err}")

    cur = mydb.cursor()

    if action == "insert" and parm1 and parm2:
                
        cur.execute(f"SELECT username FROM users")
        fetched = cur.fetchall()
        mydb.commit()                   
        
        for one_row in fetched:
            if one_row[0] == parm1:
                return "duplicate user"
            
        try:
            cur.execute(f"SELECT COUNT(*) FROM animals")
            random_animal = randint(1,cur.fetchone()[0])
            print(random_animal)
            cur.execute(f"INSERT INTO users(username, password, last_3, points, animals) VALUES('{parm1}','{parm2}','', 10,'{random_animal}')")
            mydb.commit()
            return True

        except mysql.connector.Error as err:
            print(f"Zaznam nebyl vlozen: {err}")
            return False

    if action == "delete" and parm1 and parm2:

        try:
            cur.execute(f"DELETE FROM users WHERE {parm1} = '{parm2}'")
            mydb.commit()

        except mysql.connector.Error as err:
            print(f"Zaznam nebyl smazan: {err}")

    if action == "fetchall":        

        try:
            if parm2 == "all_users":
                cur.execute(f"SELECT username from users order by id")
            if parm2 == "animals":
                cur.execute(f"SELECT animals from users where username = '{parm1}'")
            if parm2 == "friends":
                cur.execute(f"SELECT friends from users where username = '{parm1}'")  
            if parm2 == "last_3":
                cur.execute(f"SELECT last_3 from users where username = '{parm1}'")              

            if parm2 == "all_users":
                fetched = cur.fetchall()
            elif parm2 == "friends":
                fetched = cur.fetchone()
            elif parm2 == "last_3":
                fetched = cur.fetchone()
                
                if fetched == None:
                    
                    return "--no opponents yet--"
            else:
                fetched = cur.fetchone()

            if parm2 == "all_users":
                return fetched
            elif parm2 == "friends":
                
                pre_sorted_fetch = str(fetched[0]).split(",")

                pre_sorted_points = []

                for i in pre_sorted_fetch:
                    cur.execute(f"select points from users where id = {i}")
                    points = cur.fetchone()
                    pre_sorted_points.append(points[0])

                help_dict = {}
                for i in range(len(pre_sorted_fetch)):
                    help_dict[f"{pre_sorted_fetch[i]}"] = pre_sorted_points[i]                
                
                pre_final = sorted(help_dict.items(), key=lambda x: x[1])                

                final = []
                for i in pre_final:
                    final.append(i[0])

                final.reverse()                

                return final
            
            elif parm2 == "last_3":

                return fetched[0]

            else:
                return fetched[0]

        except mysql.connector.Error as err:
            print(f"Nepovedlo se LAST 3: {err}")

    if action == "fetch":
        
        try:
            if parm2 == "all_users":
                cur.execute(f"SELECT id,username from users where username = '{parm1}'")                  
            elif parm2  == "friends":       
                cur.execute(f"SELECT username,points from users where id = '{parm1}'")
            elif parm2  == "last_3":
                if parm1 == "nobody":
                    return "--no opponents yet--"
                
                cur.execute(f"SELECT username,points from users where id = '{parm1}'")         
            else:                
                cur.execute(f"SELECT username from users where id = '{parm1}'")

            fetched = cur.fetchone()
            mydb.commit()
            
            if parm2 == "all_users":
                return f"{fetched[0]} - {fetched[1]}"
            elif parm2 == "friends":
                counting_letters = len(fetched[0]) + len(str(fetched[1]))
                spaces = 30 - len(fetched[0]) #counting_letters
                return f"{fetched[0]} ({fetched[1]})"
            
            elif parm2 == "last_3":
                counting_letters = len(fetched[0]) + len(str(fetched[1]))
                spaces = 30 - len(fetched[0]) #counting_letters
                return f"{fetched[0]} ({fetched[1]})"

            else:
                return fetched[0]        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se FETCH: {err}")

    if action == "get_full_user":
        
        try:            
            cur.execute(f"SELECT * from users where username = '{parm1}'")                  

            fetched = cur.fetchone()            
        
            return fetched        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET FULL USER: {err}")

    if action == "get_full_user_ff":
        
        try:            
            cur.execute(f"SELECT * from users where username = '{parm1}'")                  

            fetched = cur.fetchone()            
        
            return fetched[0]        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET FULL USER: {err}")
    
    if action == "get_animal":
        
        try:            
            cur.execute(f"SELECT * from animals where pic = '{parm1}'")                  

            fetched = cur.fetchone()            
        
            return fetched        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET FULL USER: {err}")

    if action == "top_10":
        
        try:            
            cur.execute(f"SELECT username,points from users order by points desc limit 8")                  

            fetched = cur.fetchall()            
        
            return fetched        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se TOP 10: {err}")

    if action == "last_3":
        
        try:            
            cur.execute(f"SELECT last_3 from users where username = '{parm1}'")                  

            fetched = cur.fetchone()            
        
            return fetched        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se LAST 30: {err}")

    if action == "search_user":
        
        try:            
            cur.execute(f"SELECT username,points from users where username = '{parm1}'")                  

            fetched = cur.fetchone()
            
            if fetched == None:
                return " "
            else:
                return f"{fetched[0]} ({fetched[1]})"        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se SEARCH USER: {err}")

    if action == "bring_animals":
        
        try:            
            cur.execute(f"SELECT animals from users where username = '{parm1}'")                  

            fetched = cur.fetchone()            
            
            return fetched[0]        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se BRING ANIMALS: {err}")

    if action == "animal_info":
        
        try:            
            cur.execute(f"SELECT pic, name from animals where pic = '{parm1}'")                  

            fetched = cur.fetchone()

            print("ANIMALS ID FETCHED:", fetched[0])
            
            return fetched[0]        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se ANIMAL INFO: {err}")   

    if action == "get_card":
        
        try:            
            cur.execute(f"SELECT animals from users where username = '{parm1}'")                  

            fetched = cur.fetchone()

            new_animals = str(parm2) + "," + fetched[0]

            cur.execute(f"UPDATE users SET animals = '{new_animals}' where username = '{parm1}'")
            cur.execute(f"UPDATE users SET points = points - 5 where username = '{parm1}'")
            
            mydb.commit()
                        
            return fetched[0]        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET CARD: {err}")   

    if action == "get_points":
    
        try:            
            cur.execute(f"SELECT points from users where username = '{parm1}'")                  

            fetched = cur.fetchone()
                        
            return fetched[0]        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET POINTS: {err}")   

    if action == "get_animal_name":
    
        try:            
            cur.execute(f"SELECT name from animals where pic = {parm1}")                  

            fetched = cur.fetchone()                        
                    
            return fetched[0]        

        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET ANIMAL NAME: {err}")  

    if action == "get_country":
    
        try:            
            cur.execute(f"SELECT * from countries where pic = {parm1}")                  

            fetched = cur.fetchall()    
                    
            return fetched      

        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET COUNTRY: {err}")  

    if action == "bring_me_the_animal":
    
        try:            
            cur.execute(f"SELECT * from animals where pic = {parm1}")                  

            fetched = cur.fetchall()    
                    
            return fetched      

        except mysql.connector.Error as err:
            print(f"Nepovedlo se BRING ME THE ANIMAL: {err}")  

    if action == "challenging":
    
        try:            
            cur.execute(f"UPDATE users SET status = 'challenging', opponent = {parm2}, country = {parm3}, list_of_animals = '{parm4}' where id = {parm1}")
            cur.execute(f"UPDATE users SET status = 'challenged', opponent = {parm1}, country = {parm3} where id = {parm2}")                  
            
            mydb.commit() 

        except mysql.connector.Error as err:
            print(f"Nepovedlo se CHALLENGING: {err}")

    if action == "challenged":
    
        try:            
            cur.execute(f"UPDATE users SET status = 'answered', list_of_animals = '{parm4}' where id = {parm1}") 
            mydb.commit() 

        except mysql.connector.Error as err:
            print(f"Nepovedlo se CHALLENGED GO: {err}")            

    if action == "cancelled_challenge":

        print("am i here?",parm2)
    
        try:            
            cur.execute(f"UPDATE users set status = 'free', country = 0, opponent = 0, list_of_animals = '' where username = '{parm1}'")
            cur.execute(f"UPDATE users set points = points - 2 where username = '{parm1}'")
            cur.execute(f"UPDATE users set status = 'free', country = 0, opponent = 0, list_of_animals = '' where username = '{parm2}'")

            mydb.commit() 
            
        except mysql.connector.Error as err:
            print(f"Nepovedlo se CANCELLED CHALLENGE: {err}") 

    if action == "rejected_challenge":
    
        try:            
            cur.execute(f"UPDATE users set status = 'free', country = 0, opponent = 0, list_of_animals = '' where username = '{parm1}'")            
            cur.execute(f"UPDATE users set status = 'rejected', country = 0, list_of_animals = '' where username = '{parm2}'")

            mydb.commit() 
            
        except mysql.connector.Error as err:
            print(f"Nepovedlo se REJECTED CHALLENGE: {err}") 

    if action == "rejected_ok":

        print("am i here?",parm2)
    
        try:            
            cur.execute(f"UPDATE users set status = 'free', country = 0, opponent = 0, list_of_animals = '' where username = '{parm1}'")            
            
            mydb.commit() 
            
        except mysql.connector.Error as err:
            print(f"Nepovedlo se REJECTED OK: {err}") 

    if action == "get_full_user_by_id":
    
        try:            
            cur.execute(f"SELECT * from users where id = {parm1}")

            fetched = cur.fetchone()  
        
            return fetched 
            
        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET FULL USER BY ID: {err}")  

    if action == "continue":
    
        try:            
            cur.execute(f"UPDATE users SET points = points + {parm2}, status = 'free', list_of_animals = '', opponent = 0, country = 0 where id = {parm1}")
            mydb.commit()
                  
        except mysql.connector.Error as err:
            print(f"Nepovedlo se GET FULL USER BY ID: {err}") 

    if action == "answered_2":
    
        try:            
            cur.execute(f"UPDATE users SET status = 'answered_2' where id = {parm1}")
            
            mydb.commit()
                  
        except mysql.connector.Error as err:
            print(f"Nepovedlo se ANSWERED 2: {err}")

    if action == "copy_opponent_for_final":
    
        try:            
            cur.execute(f"UPDATE users SET user_ff='{parm2}',user_scoring='{parm3}',user_total_points={parm4},opponent_ff='{parm5}',opponent_scoring='{parm6}',opponent_total_points={parm7},final_country='{parm8}',user_animals='{parm9}',opponent_animals='{parm10}' where id = {parm1}")
            
            mydb.commit()
                  
        except mysql.connector.Error as err:
            print(f"Nepovedlo se COPY OPPONENT FOR FINAL: {err}")

    if action == "clean_user":
    
        try:            
            cur.execute(f"UPDATE users SET country = 0, opponent = 0, user_ff='',user_scoring='',user_total_points='',opponent_ff='',opponent_scoring='',opponent_total_points='',final_country='',user_animals='',opponent_animals='' where id = {parm1}")
            
            mydb.commit()
                  
        except mysql.connector.Error as err:
            print(f"Nepovedlo se ANSWERED 2: {err}")
    
    if action == "count_the_animals":
    
        try:            
            cur.execute(f"select count(*) from animals")
            
            fetched = cur.fetchone()

            return fetched[0]
                  
        except mysql.connector.Error as err:
            print(f"Nepovedlo se COUNT ANIMALS: {err}")

    if action == "get_countries_count":
    
        try:            
            cur.execute(f"select count(*) from countries")
            
            fetched = cur.fetchone()

            return fetched[0]
                  
        except mysql.connector.Error as err:
            print(f"Nepovedlo se COUNT COUNTRIES: {err}")

    if action == "count_the_animals":
    
        try:            
            cur.execute(f"select count(*) from animals")
            
            fetched = cur.fetchone()

            return fetched[0]
                  
        except mysql.connector.Error as err:
            print(f"Nepovedlo se COUNT ANIMALS: {err}")

    if action == "last_3_update":
    
        try:            
            cur.execute(f"select last_3 from users where id = {parm1}")            
            fetched = cur.fetchone()

            last3 = fetched[0].split(",")

            if str(parm2) in last3:
                last3.remove(str(parm2))

            last3.insert(0,f"{parm2}"+",")

            if len(last3) >= 4:
                del last3[-1]

            slast3 = ""

            slast_nr = -1
            for item in last3:
                slast_nr += 1
                if slast_nr == 0:
                    slast3 += str(item)
                else:
                    slast3 += str(item)+","

            slast3 = slast3.strip(",")

            cur.execute(f"UPDATE users SET last_3 = '{slast3}' where id = {parm1}")            
            mydb.commit()

            return fetched[0]
                  
        except mysql.connector.Error as err:
            print(f"Nepovedlo se SLAST3: {err}")    

    if action == "login" and parm1 and parm2:

        try:
            cur.execute(f"SELECT * from users")

            fetched = cur.fetchall()
            mydb.commit()
            
            for row in fetched:
                if row[1] == parm1:
                    if parm2 == row[2]:
                        print(f"uspesne prihlaseni, vitej {row[1]}!")
                        return True
                    else:
                        print("Neplatne heslo! Zkus to znovu!")
                        return False

        except mysql.connector.Error as err:
            print(f"Nepovedlo se LOGIN: {err}") 