#Goldfish game
import time
from random import random
rankDic={0:'[A]', 10:'[J]', 11:'[Q]',12:'[K]'}
rankRevDic={'A':0,'J':10,'Q':11,'K':12}
printd=False
person=True


#Link to skype?
#Graphics plz (pyqt?)
#What is the object oriented way of doing this?

def isInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def printi(s):
    if printd==True:
        print(s)
        
def genDeck():
    deck=[]
    for i in range(52):
        deck.append(i)
    return deck

def genHand():
    hand=[]
    for i in range(13):
        hand.append(0) #Creates data structure of frequency (rank is index)
    return hand

def drawCard(pHand,deck,nCards=1):
    #As of now, no suit support
    #suitDic=['Spades', 'Heart', 'Clover', 'Diamonds']
    
    pHand[deck.pop(int(random()*len(deck)))%13]+=1
    if nCards==1:
        return
    elif nCards>1:
        return drawCard(pHand,deck,nCards-1)
    else:
        raise ValueError('Cards drawn less than 1')
        
def dispCard(rank):
        if rank in [0,10,11,12]:
            return rankDic[rank]
        else:
            return'['+str(rank+1)+']'
        
def dispHand(pHand,p1score,p2score,pName='Player 1'):
    printi("Score: (Player 1 has %s stacks) vs. (Player 2 has %s stacks)" % (p1score, p2score))
    response= pName+' hand:'
        
    for i in range(13): #Print hand
        nRank=pHand[i]     
        if nRank>0:
            response +=' '+str(nRank)+'x '+dispCard(i)+','
            
    printi(response[:-1]+'.')
    
def p1Move(p1,p1score,p2score):
    dispHand(p1,p1score,p2score)
    
    while True:
        #Convert to Numbers
        choice=raw_input("What card do you want to ask for?  >> ")
        if choice in ['A','a','J','j','Q','q','K','k']:
            choice=rankRevDic[choice.capitalize()]
        elif isInt(choice):
            choice=int(choice)-1
        elif choice=="break":
            return "break"
        elif choice=="hand":
            return "hand"
        
        #Check validity of choice    
        if choice in range(13):                 
            if p1[choice]>0 and p1[choice]<4:
                return choice
            else:
                printi("You don't have that card! Choose another card.")
        elif choice == None and sum(p1)==0:
            return choice
        else:
            printi("That card doesn't exist. Try again.")

    
    
def p2Move(p2,p1score,p2score):
    while True:
        choice=int(random()*13)
        if p2[choice]>0 and p2[choice]<4:
            return choice
        elif sum(p2)==0:
            return None
            
def main():
    p1=genHand()
    p2=genHand()
    p1score=0
    p2score=0
    startnCards=7
    deck=genDeck()
    nMove=0
    
    #Draw Cards
    drawCard(p1,deck,startnCards)
    drawCard(p2,deck,startnCards)
    
    #Play the Game
    while len(deck)>0 and (len(p1)>0 or len(p2)>0):
        nMove+=1
        if nMove%2==1:
            choice = p2Move(p1,p1score,p2score)
            if choice == "break":
                return
            elif choice == "hand":
                print(p1)
                print(p2)
                print(len(deck))
                return
            elif not choice:
                drawCard(p1,deck,1)
            elif p2[choice]>0 and p2[choice]<4:
                printi("It's in his hand!Go again!\n")
                while p2[choice]>0:
                    p2[choice]-=1
                    p1[choice]+=1
                printi(p1[choice])
                printi(p2[choice])
                nMove-=1
            else:
                printi("It's not in his hand. Go Fish.\n")
                drawCard(p1,deck,1) #Note that if you draw the card that you wanted, you do not get another turn
        else:
            time.sleep(0)
            choice = p2Move(p2,p1score,p2score)
            if not choice:
                drawCard(p1,deck,1)
            elif p1[choice]>0 and p1[choice]<4:
                printi("Player Two took"+dispCard(choice)+"!!\n")
                while p1[choice]>0:
                    p1[choice]-=1
                    p2[choice]+=1
                if p2[choice] == 4:
                    p2[choice] -= 4
                    p2score+=1
                nMove-=1
            else:
                printi("Player Two GO FISH for asking for a "+ dispCard(choice) +".\n")
                drawCard(p2,deck,1)                
        
        for i in range(13):
            if p1[i] == 4:
                p1[i] -= 4
                p1score+=1
            if p2[i] == 4:
                p2[i] -= 4
                p2score+=1
    if person:
        print("\nThe final score is %d to %d" % (p1score,p2score))
        if p1score>p2score:
            printi("Congratulations, you win!")
        elif p1score<p2score:
            printi("You Lost!")
        else:
            printi("It's a Tie!")
            
        replay=raw_input("Wanna play again? ")
        if replay in ['y','Y','Yes','yes']:
            main()    
    else:
        if p1score>p2score:
            return 1
        elif p1score<p2score:
            return -1
        else:
            return 0
main()