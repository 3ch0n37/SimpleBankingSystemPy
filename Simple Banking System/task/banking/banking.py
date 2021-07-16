import utils
from bank import Bank


def main():
    current_account = False
    stop = False
    bank = Bank()
    while not stop:
        if not current_account:
            choice = utils.menu()
            if choice == 1:
                new = bank.new_account()
                print('\nYour card has been created')
                print('Your card number:')
                print(new.account_number)
                print('Your card PIN:')
                print(new.pin)
                print()
            elif choice == 2:
                number = input('\nEnter your card number:\n')
                pin = input('Enter your PIN:\n')
                account = bank.find_account(number)
                if account and account.login(number, pin):
                    print('\nYou have successfully logged in!')
                    current_account = account
                else:
                    print('\nWrong card number or PIN!')
            elif choice == 0:
                break
            else:
                print('\nWrong option!\n')
        else:
            choice = utils.account_menu()
            if choice == 1:
                print(f'\nBalance: {current_account.balance}')
            elif choice == 2:
                try:
                    income = int(input('Enter income:\n'))
                except ValueError:
                    print('Not a number!')
                    continue
                if bank.add_income(current_account, income):
                    print('Income was added!')
                    current_account = bank.find_account(current_account.account_number)
                else:
                    print('There was an error while adding income!')
            elif choice == 3:
                print('\nTransfer')
                reciever = input('Enter card number:\n')
                if len(reciever) != 16 or utils.luhns(reciever) != int(reciever[-1]):
                    print('Probably you made a mistake in the card number. Please try again!')
                    continue
                send_to = bank.find_account(reciever)
                if not send_to:
                    print('Such a card does not exist!')
                    continue
                try:
                    amount = int(input('Enter how much money you want to transfer:\n'))
                except ValueError:
                    print('Not a number!')
                    continue
                res = bank.do_transfer(current_account, send_to, amount)
                if res == -1:
                    print('Not enough money!\n')
                elif res == 0:
                    print('Same account!\n')
                elif res is True:
                    print('Success!')
                    current_account = bank.find_account(current_account.account_number)
                else:
                    print('There was an error while doing the transfer!')
            elif choice == 4:
                if bank.close_account(current_account):
                    current_account = False
                    print('The account has been closed!')
                else:
                    print("Couldn't close your account!")
            elif choice == 5:
                current_account = False
                print('\nYou have successfully logged out!\n')
            elif choice == 0:
                break
            else:
                print('\nWrong option!\n')
    print('\nBye!')


if __name__ == '__main__':
    main()
