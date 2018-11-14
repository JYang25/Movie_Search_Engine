from app import app, Movies, Index
from Query_Evaluation import QueryEvaluation
from recomm import recommTop20,recommByGenre

def main():
 choice ='0'
 query = ''
 user_id = '0'
 while choice =='0':
    print("Movie Club : ")
    if user_id == '0':
        print("1. Login")
    elif user_id != '0':
        print("1. Movie search")
        print("2. Top 20 recommended movies")
        print("3. Recommend by genres")
        print("4. Logout")

    choice = input ("Please make a choice: ")

    if user_id == '0':
        if choice == '1':
            user_id = input ("User: ")
    else:
        if choice == '1':
            while (query != 'q'):
                query = input ("Search: (type q to quit search)")
                result_list = QueryEvaluation(query, Index, Movies)  
                for m in result_list:
                    print(f' -  [{m[1]}] | Director: {m[3]} | Star: {m[2]} | Recommend(0-5): {m[5]}')
        elif choice == '2':
            recommend_list = recommTop20(user_id)
            for m in recommend_list:
                if str(m[0]) in M:
                    print(f' -  [{M[str(m[0])].GetTitle()}] | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommend(0-5): {m[1]}')
        elif choice == '3':
            genres_menu()
        elif choice == '4':
            print(f'User{user_id} logout.')
            user_id = 0
        else:
            print("I don't understand your choice.")
    choice = '0'

def genres_menu():
    genres_choice = '0'
    while genres_choice =='0':
         print("1. Comedy")
         print("2. Horror")
         print("3. Fantasy")
         print("4. Back to main menu")
         genres_choice = input ("Recommend by : ")
         if genres_choice == '1':
            recommend_list = recommByGenre(user_id, "Comedy")
            for m in recommend_list:
                if str(m[0]) in M:
                    print(f' -  [{M[str(m[0])].GetTitle()}] | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommend(0-5): {m[1]}')
         elif genres_choice == '2':
            recommend_list = recommByGenre(user_id, "Horror")
            for m in recommend_list:
                if str(m[0]) in M:
                    print(f' -  [{M[str(m[0])].GetTitle()}] | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommend(0-5): {m[1]}')
         elif genres_choice == '3':
            recommend_list = recommByGenre(user_id, "Fantasy")
            for m in recommend_list:
                if str(m[0]) in M:
                    print(f' -  [{M[str(m[0])].GetTitle()}] | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommend(0-5): {m[1]}')
         elif genres_choice == '4':
            break
         else:
            print("I don't understand your choice.")
         genres_choice = '0'

main()
