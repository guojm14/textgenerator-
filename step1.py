# -*- coding: utf-8 -*-
  
import os
import pygame
fontlist=os.listdir('chinese_font')

pygame.init()

textline = open('text.txt').readlines()
def rend(text,fontlist,fontpath,name):
    numfont=len(fontlist)
    text=unicode(text, "utf-8")
    for i in xrange(numfont):
        font = pygame.font.Font(os.path.join(fontpath,fontlist[i]), 63)
        rtext = font.render(text, True, (255, 255, 255), (0, 0, 0))
  
        pygame.image.save(rtext, 'result/'+name+'_'+str(i)+".jpg")
count=0
for item in textline:
    text=item.strip().split(',')[0]
    if len(text)>=5:
        rend(text,fontlist,'chinese_font',str(count))
        count+=1
