from app import app, Movies, Index
from Process_Metadata import M
from Query_Evaluation import QueryEvaluation
from recomm import recommTop20,recommByGenre



def mainMenu():
 choice ='0'
 user_id = '0'

 while choice =='0':
    print()
    print("-------------------------")
    print("  Welcome to Movie Club")
    print("-------------------------")
    if user_id == '0':
        print("1. Login")
        print("2. Exit")
    elif user_id != '0':
        print("1. Movie search")
        print("2. Top 10 recommended movies")
        print("3. Recommend by genres")
        print("4. Logout")

    choice = input ("Please make a choice: ")

    if user_id == '0':
        if choice == '1':
            user_id = input ("User: ")
        elif choice =='2':
            print("Bye-bye.")
            break
    else:
        if choice == '1':
            searchMenu(user_id)
        elif choice == '2':
            recommendMenu(user_id)
        elif choice == '3':
            genresMenu(user_id)
        elif choice == '4':
            print(f'User{user_id} logout.')
            user_id = '0'
        else:
            print("I don't understand your choice.")
    choice = '0'

def recommendMenu(userid):
    user_id = userid
    metric_choice = '0'
    while metric_choice =='0':
         print()
         print("1. Cosine")
         print("2. Pearson")
         print("3. Euclidean")
         print("4. Back to main menu")
         metric_choice = input ("Similarity metric by : ")
         if metric_choice == '1':
            recommend_list = recommTop20(user_id, "cosine")
         elif metric_choice == '2':
            recommend_list = recommTop20(user_id, "pearson")
         elif metric_choice == '3':
            recommend_list = recommTop20(user_id, "euclidean")
         elif metric_choice == '4':
            break
         else:
            print("I don't understand your choice.")
         count = 0
         for m in recommend_list:
            if count == 10:
                break
            if str(m[0]) in M:
                count += 1
                print(f' -  [{M[str(m[0])].GetTitle()}] | Genres: {M[str(m[0])].GetGenres()} | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommendation Rate(0-5): {m[1]}')
         metric_choice = '0'

def searchMenu(userid):
    user_id = userid
    query = ''
    search_choice = '0'
    while search_choice =='0':
         print()
         print("1. TF-IDF")
         print("2. Probability Model")
         print("3. Back to main menu")
         search_choice = input ("Search by : ")
         if search_choice == '1':
            while (query != 'q'):
                query = input ("Search(type q to quit search): ")
                result_list = QueryEvaluation(query, Index, Movies, user_id, "tf-idf")  
                for m in result_list:
                    print(f' -  [{m[2]}] | Genres:{m[1]} | Director: {m[4]} | Star: {m[3]} | Recommendation Rate(0-5): {m[6]}')
         elif search_choice == '2':
            while (query != 'q'):
                query = input ("Search(type q to quit search): ")
                result_list = QueryEvaluation(query, Index, Movies, user_id, "language-model")  
                for m in result_list:
                    print(f' -  [{m[2]}] | Genres:{m[1]} | Director: {m[4]} | Star: {m[3]} | Recommendation Rate(0-5): {m[6]}')
         elif search_choice == '3':
            break
         else:
            print("I don't understand your choice.")
         query = ''
         search_choice = '0'

def genresMenu(userid):
    user_id = userid
    genres_choice = '0'
    while genres_choice =='0':
         print()
         print("1. Action")
         print("2. Comedy")
         print("3. Drama")
         print("4. Horror")
         print("5. Back to main menu")
         genres_choice = input ("Recommend by : ")
         if genres_choice == '1':
            recommend_list = recommByGenre(user_id, "Action")
            for m in recommend_list:
                if str(m[0]) in M:
                    print(f' -  [{M[str(m[0])].GetTitle()}] | Genres: {M[str(m[0])].GetGenres()} | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommendation Rate(0-5): {m[1]}')
         elif genres_choice == '2':
            recommend_list = recommByGenre(user_id, "Comedy")
            for m in recommend_list:
                if str(m[0]) in M:
                    print(f' -  [{M[str(m[0])].GetTitle()}] | Genres: {M[str(m[0])].GetGenres()} | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommendation Rate(0-5): {m[1]}')
         elif genres_choice == '3':
            recommend_list = recommByGenre(user_id, "Drama")
            for m in recommend_list:
                if str(m[0]) in M:
                    print(f' -  [{M[str(m[0])].GetTitle()}] | Genres: {M[str(m[0])].GetGenres()} | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommendation Rate(0-5): {m[1]}')
         elif genres_choice == '4':
            recommend_list = recommByGenre(user_id, "Horror")
            for m in recommend_list:
                if str(m[0]) in M:
                    print(f' -  [{M[str(m[0])].GetTitle()}] | Genres: {M[str(m[0])].GetGenres()} | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommendation Rate(0-5): {m[1]}')
         elif genres_choice == '5':
            break
         else:
            print("I don't understand your choice.")
         genres_choice = '0'

