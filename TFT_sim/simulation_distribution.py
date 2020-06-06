#Just For Fun!!!
#Please feel free to contact me if you have any interesting ideas about this code
#E-mail:    790535475@qq.com
#           Haoycupc@gmail.com
import numpy as np
import matplotlib.pyplot as plt
import os
import pygame
from pygame.locals import *
from sys import exit


# Constants
pygame.init()
screen = pygame.display.set_mode((1600, 900), 0, 32)
pygame.display.set_caption("TFT_simulation")

screen.fill((240,255,240))
id=1
f=pygame.font.Font(None,70)
fps=20
round=0



# Constants for Teamfight Tactics patch 10.11
possibility = {2: [1, 0, 0, 0, 0], 3: [0.75, 0.25, 0, 0, 0], 4: [0.55, 0.3, 0.15, 0, 0],
               5: [0.4, 0.35, 0.2, 0.05, 0], 6: [0.25, 0.35, 0.3, 0.1, 0], 7: [0.19, 0.3, 0.35, 0.15, 0.01],
               8: [0.14, 0.2, 0.35, 0.25, 0.06], 9: [0.1, 0.15, 0.25, 0.35, 0.15]}

# Names of comps
compsname = ('BrawBla','VoidBrawSor','VanSniper','Rebel','BladeMaster','Cybernetic','DrakStar','Priate')

listwin=[0,0,0,0,0,0,0,0]

plt.ion()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

times=0

namelist = ['JarvanIV', 'Malphite', 'Zoe', 'Leona', 'Poppy', 'Graves', 'Xayah', 'Fiora', 'KhaZix',
         'TwistedFate',
         'Caitlyn', 'Ziggs','Sona', 'XinZhao', 'Yasuo', 'Mordekaiser', 'Annie', 'Blitzcrank', 'Shen', 'Ahri', 'Darius',
         'Lucian',
         'KaiSa', 'Rakan','Karma', 'MasterYi', 'Kassadin', 'Rumble', 'Lux', 'Ezreal', 'Vi', 'Jayce', 'Ashe', 'Shaco',
         'Syndra','Soraka', 'Jinx', 'Fizz', 'WuKong', 'Jhin', 'VelKoz', 'Kayle', 'Irelia', 'ChoGath','Lulu', 'MissFortune', 'AurelionSol', 'Gangplank', 'Ekko', 'Thresh', 'Xerath']

#The comps for 8 players
compslist=[{'Malphite':3,'Lucian':3,'Blitzcrank':3, 'Ezreal':3,'MissFortune':1,'Vi':3,'ChoGath':3,'Jinx':9,'Graves':3},
            {'Malphite':3,'ChoGath':3,'VelKoz':9,'KhaZix':3,'Vi':3,'Blitzcrank':3,'TwistedFate':3,'Fizz':3},
            {'Ashe':3,'Jayce':3,'Karma':3,'Jhin':9,'Poppy':3,'WuKong':3,'Mordekaiser':3,'Lulu':1},
           {'MasterYi':3,'Ziggs':3, 'AurelionSol':1,'Yasuo':3, 'Jinx':9,'MissFortune':1,'Gangplank':1,'Lulu':1,'Sona':3},
            {'MasterYi':3,'Kayle':9, 'Irelia':3,'Yasuo':3, 'Fiora':3,'Xayah':3,'Shen':3,'Kassadin':3,'MissFortune':1},
            { 'Leona':3,'Lucian':3, 'Irelia':9,'Vi':3, 'Fiora':3,'Ekko':1,'Shen':3,'Kassadin':3,'Thresh':1},
            {'JarvanIV':3,'Shaco':3,'Karma':3,'Jhin':9,'Lux':3,'Mordekaiser':3,'Lulu':1,'Xerath':1},
           {'Gangplank':3,'Graves':3,'Darius':9,'Jayce':3,'XinZhao':3,'Ashe':3,'Kassadin':3,'Rakan':3}]

#Pics

pics=[]
for eachchamp in namelist:
    pics.append(pygame.image.load(os.path.dirname(__file__)+'/icon/'+eachchamp+'.png'))

idlist=[]
for eachid in range(8):
    idlist.append(pygame.image.load(os.path.dirname(__file__)+'/id/'+str(eachid+1)+'.png'))
starslist=[]
for eachstar in range(3):

    surface=pygame.image.load(os.path.dirname(__file__) + '/star' + str(eachstar + 1) + '.png')


    starslist.append(pygame.transform.scale(surface,(64, 20)))



clock=pygame.time.Clock()
# New round() defines the different actions the player will take under different circumstances
class Player():
    def __init__(self,ids,comps,idealrank,idealgolds):
        self.comps = comps.copy()
        self.golds=1
        self.rank=2
        self.exp=0
        self.exp_limit={2:2,3:6,4:10,5:20,6:32,7:50,8:66}
        self.pool=dict() #This is Your deck
        self.idealrank= idealrank
        self.idealgolds = idealgolds
        self.ids=ids

        self.myfont = pygame.font.Font(None, 35)
    def cost(self,price):
        if self.golds>=price:
            self.golds = self.golds - price

            textImage = self.myfont.render('Golds: '+str(self.golds)+' ', True, (0, 0, 0),(222,255,222))
            screen.blit(textImage,(1300,94*self.ids))
            return True
        else:
            return False
    def Buy_champ_tastics(self,champ_name,tiers,cp):

        if champ_name in self.comps: # comps check
            if self.golds>=tiers:    # consume strategic
                    #
                champ_num=self.pool.get(champ_name,0) #check champ_num,if there is no this champ in your deck , return 0.
                if champ_num <=self.comps.get(champ_name):

                    self.cost(tiers)
                    self.pool.update({champ_name:champ_num+1})
                    #print('Buy ',champ_name,', And you have',champ_num+1,'of that')
                   # print(cp[tiers].count(champ_name))
                    cp[tiers].remove(champ_name) #remove champ from commonpool
                if champ_num== 9:
                    pass
        return cp


    def  roll(self,commonpool,possibility):
        # Tier randomness
        card_possibility_list = possibility.get(self.rank)  # listofeahctier
        card_dict=[]
        for cards in range(5):#
            tiers=np.random.choice([1,2,3,4,5],p=card_possibility_list) # get the tier of a card.
            champ_name=np.random.choice(commonpool[tiers])#get a random champ nam
            card_dict.append((champ_name,tiers))
            #print(card_dict)
        card_dict.sort(key=lambda card_dict:card_dict[1],reverse=True) # sort cards by tiers
        #print(card_dict)
        #shop
        shoporder=1
        for each in card_dict:

            shopcard = namelist.index(each[0])
            x = (shoporder) * 66+580+290
            y = (self.ids-1) * 64+30*self.ids+64
            screen.blit(pics[shopcard], (x, y))
            shoporder=shoporder+1

        for champ_tier in card_dict:
           # print(champ_tier[0], champ_tier[1])
           ## print(commonpool[tiers].count(champ_name))
            commonpool=self.Buy_champ_tastics(champ_tier[0], champ_tier[1], commonpool) # check comps,and decide buy this card or not
        allchamp=self.pool.keys()

        champorder=1
        for eachchamp in allchamp: #max == 8
            order=namelist.index(eachchamp)
            champnum_3=self.pool.get(eachchamp,0)//3 #0,1,2
            x=(champorder)*66+20*(champorder+1)
            y = (self.ids-1) * 64+30*self.ids+64
            screen.blit(pics[order], (x,y))

            ystar=  94* self.ids+64-20
            if champnum_3==0:
                starnum=0
            elif champnum_3==1 or champnum_3==2:
                starnum=1
            elif champnum_3==3:
                starnum=2
            screen.blit(starslist[starnum], (x, ystar))
            champorder=champorder+1

        pygame.display.update()
        return commonpool


    def experiance(self):

        if self.rank==5:
            self.exp_limit.keys(2)
    def new_round(self,round_num,commonpool,possibility):
    # Ready Pahse

        if self.rank<9:
            exp_max = self.exp_limit.get(self.rank)
            if self.exp > exp_max:
                self.exp = self.exp - exp_max
                self.rank = self.rank + 1
               # print('level up',self.rank)

                textImage = self.myfont.render('Rank: ' + str(self.rank) + ' ', True, (0, 0, 0), (222, 255, 222))
                screen.blit(textImage, (1500, 94 * self.ids))

        if round_num == 1:
            pass
        elif round_num<=4:
            self.cost(-2)
        elif round_num==5:
            self.cost(-3)
        elif round_num == 6:
            self.cost(-4)
        elif round_num >= 7:
            self.cost(-5)


        commonpool=self.roll(commonpool,possibility)

    # Level-up and re-roll strategies
        while 1:


                if self.rank <7 and len(self.pool) < self.rank:
                        if self.golds>=20:

                            self.cost(2)
                            commonpool=self.roll(commonpool, possibility)
                        else:
                            break


                elif self.rank < self.idealrank:
                    if self.golds > self.idealgolds:
                        self.cost(4)
                        self.exp = self.exp + 4
                        exp_max = self.exp_limit.get(self.rank)
                        if self.exp > exp_max:
                            self.exp = self.exp - exp_max
                            self.rank = self.rank + 1
                            textImage = self.myfont.render('Rank: ' + str(self.rank) + ' ', True, (0, 0, 0),
                                                           (222, 255, 222))
                            screen.blit(textImage, (1500, 94 * self.ids))
                            break
                    else:
                        break
                else:

                    if self.golds>4:
                        self.cost(2)
                        commonpool=self.roll(commonpool,possibility)
                    else:
                        break



    # End Phase
        if self.golds // 10 != 0:
            self.cost(-1 * (self.golds // 10))
        if self.rank<9:
            self.exp = self.exp + 2
        return commonpool


while True:
    tier1 = ['JarvanIV', 'Malphite', 'Zoe', 'Leona', 'Poppy', 'Graves', 'Xayah', 'Fiora', 'KhaZix',
             'TwistedFate',
             'Caitlyn', 'Ziggs'] * 29
    tier2 = ['Sona', 'XinZhao', 'Yasuo', 'Mordekaiser', 'Annie', 'Blitzcrank', 'Shen', 'Ahri', 'Darius',
             'Lucian',
             'KaiSa', 'Rakan'] * 22  # green
    tier3 = ['Karma', 'MasterYi', 'Kassadin', 'Rumble', 'Lux', 'Ezreal', 'Vi', 'Jayce', 'Ashe', 'Shaco',
             'Syndra'] * 16  # blue
    tier4 = ['Soraka', 'Jinx', 'Fizz', 'WuKong', 'Jhin', 'VelKoz', 'Kayle', 'Irelia', 'ChoGath'] * 12
    tier5 = ['Lulu', 'MissFortune', 'AurelionSol', 'Gangplank', 'Ekko', 'Thresh', 'Xerath'] * 10
    times=times+1
    round=0
    playerlist=[]
    id=1
    commonpools = [np.nan, tier1.copy(), tier2.copy(), tier3.copy(), tier4.copy(), tier5.copy()]
    roundover=0
    for eachplayer in compslist:
        playerlist.append(Player(id,eachplayer, idealrank=8, idealgolds=40))
        id=id+1
       # print(id)

    for eachplayer in playerlist:
        print(eachplayer.pool,eachplayer.golds)

    plt.clf()
    for round in range(74)[1:]:
        screen.fill((222,255,222))
        for event in pygame.event.get():
            if event.type == QUIT:

                exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:


                    fps=fps+10
                if event.key == K_RIGHT:
                    fps = fps + 10
                if event.key == K_SPACE:
                    k=1
                    while k:
                        for event in pygame.event.get():
                            #print(event)
                            if event.type == KEYDOWN:
                                if event.key == K_SPACE:
                                    k=0
                                    break




        round=round+1
        if round<=4:
            state='1-'+str(round)+'                             '
        else: state= str((round-4)//7+2)+'-'+str((round-4)%7+1)

        text=f.render(state,True,(0,0,0),(222,255,222))

        screen.blit(text, (630, 10))
        for eachplayer in playerlist:

            screen.blit(idlist[eachplayer.ids-1], (0, (eachplayer.ids-1) * 94+64))
            commonpools=eachplayer.new_round(round + 1, commonpools, possibility)
            p=[]
            c=[]
            if eachplayer.pool.keys() == eachplayer.comps.keys():
                for each in eachplayer.pool.keys():
                    p.append(eachplayer.pool.get(each))
                    c.append(eachplayer.comps.get(each))
                check=np.array(p)-np.array(c)>=0

                if False not in check:


                    listwin[eachplayer.ids-1]=listwin[eachplayer.ids-1]+1
                    roundover=1
                    break


        if roundover == 1:

            break
    result = plt.subplot(1, 1, 1)

    result.set_title('Test:' + str(times))
    print(times)
    result.bar(compsname, listwin)
    plt.pause(0.001)
plt.show()













