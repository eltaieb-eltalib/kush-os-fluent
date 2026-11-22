#!/usr/bin/env python3
"""Build KushFluent from the existing GPLv3 Modern theme, with original flat parts."""
from pathlib import Path
from PIL import Image, ImageDraw
import shutil,re
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'media/themes/Modern/modern.msstyles'
OUT=ROOT/'media/themes/KushFluent/kushfluent.msstyles'
if not OUT.exists(): shutil.copytree(BASE,OUT)
(OUT.parent/'CMakeLists.txt').write_text('add_subdirectory(kushfluent.msstyles)\n')
p=OUT/'CMakeLists.txt';s=(BASE/'CMakeLists.txt').read_text().replace('modern','kushfluent').replace('${CMAKE_CURRENT_BINARY_DIR}/bitmaps/*', '${CMAKE_CURRENT_SOURCE_DIR}/bitmaps/*').replace('${CMAKE_CURRENT_BINARY_DIR}/lang/*', '${CMAKE_CURRENT_SOURCE_DIR}/lang/*').replace('${CMAKE_CURRENT_BINARY_DIR}/textfiles/*', '${CMAKE_CURRENT_SOURCE_DIR}/textfiles/*');p.write_text(s)
p=OUT/'kushfluent.rc';s=(BASE/'modern.rc').read_text().replace('Modern Theme','Kush Fluent Theme').replace('"Modern\\0"','"KushFluent\\0"').replace('modern.msstyles','kushfluent.msstyles');p.write_text(s)
(OUT/'modern.rc').unlink(missing_ok=True)
for p in (OUT/'textfiles/Light').glob('*.INI'):
 s=p.read_text()
 if '[Button.Pushbutton]\nTransparent = True' not in s:
  s=s.replace('[Button.Pushbutton]','[Button.Pushbutton]\nTransparent = True\nTransparentColor = 255 0 255')
 s=re.sub(r'Tahoma,\s*(8|9)', 'Inter, 9', s, flags=re.I)
 s=re.sub(r'CaptionFont\s*=.*', 'CaptionFont = Inter SemiBold, 9', s)
 changes={'ActiveCaption':'243 246 250','InactiveCaption':'246 247 249','GradientActiveCaption':'243 246 250','GradientInactiveCaption':'246 247 249','CaptionText':'30 35 41','InactiveCaptionText':'117 123 132','Btnface':'247 248 250','MenuBar':'247 248 250','Highlight':'13 115 119','HighlightText':'255 255 255','MenuHilight':'221 240 239','CaptionBarHeight':'28','TextShadowOffset':'0,0','TextShadowColor':'243 246 250'}
 for key,value in changes.items(): s=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,s)
 # A pale client background for themed dialogs, without changing their layout.
 s=s.replace('BorderColor = 239 238 243','BorderColor = 247 248 250').replace('FillColor = 239 238 243','FillColor = 247 248 250')
 # The pale Kush taskbar needs dark clock text, unlike the inherited Modern tray.
 s=re.sub(r'(\[TrayNotify::Clock\][^\[]*?TextColor\s*=\s*)[^\n]*',r'\g<1>30 35 41',s)
 s=s.replace('TextColor = 127 124 115','TextColor = 30 35 41')
 s=s.replace('EdgeShadowColor = 165 175 185','EdgeShadowColor = 226 231 237')
 s=s.replace('BorderColor = 150 150 150','BorderColor = 202 208 216')
 for part in ['ScrollBar.GripperHorz','ScrollBar.GripperVert']:
  token='['+part+']'
  start=s.find(token);end=s.find('\n[',start+1)
  if start >= 0:
   end=len(s) if end < 0 else end
   section=s[start:end]
   if 'TransparentColor' not in section:s=s[:start]+section+'\nTransparentColor = 255 0 255\n'+s[end:]
 p.write_text(s)
B=OUT/'bitmaps/Light'
MAG=(255,0,255); ACTIVE=(243,246,250); INACTIVE=(246,247,249); BORDER=(202,208,216)
def frames(name, states=2, kind='top'):
 p=B/('LIGHT_'+name+'.bmp'); old=Image.open(p);w,h=old.size; sh=h//states
 im=Image.new('RGB',(w,h),MAG)
 for i in range(states):
  tile=Image.new('RGB',(w,sh),MAG);d=ImageDraw.Draw(tile);fill=ACTIVE if i==0 else INACTIVE
  if kind=='top':d.rounded_rectangle((0,0,w-1,sh+15),radius=7,fill=fill,outline=BORDER,width=1)
  elif kind=='bottom':d.rounded_rectangle((0,-15,w-1,sh-1),radius=7,fill=fill,outline=BORDER,width=1)
  else:
   d.rectangle((0,0,w-1,sh-1),fill=fill);x=0 if kind=='left' else w-1;d.line((x,0,x,sh-1),fill=BORDER)
  im.paste(tile,(0,i*sh))
 im.save(p)
for n in ['FRAMECAPTION','FRAMECAPTIONSIZING','FRAMECAPTIONMIN','SMALLFRAMECAPTION','SMALLFRAMECAPTIONSIZING','FRAMEMAXIMIZED']:
 frames(n)
frames('FRAMEBOTTOM',kind='bottom');frames('FRAMELEFT',kind='left');frames('FRAMERIGHT',kind='right')
def buttons(name,count,caption=False,close=False):
 p=B/('LIGHT_'+name+'.bmp');w,h=Image.open(p).size;sh=h//count;im=Image.new('RGB',(w,h),MAG)
 for i in range(count):
  tile=Image.new('RGB',(w,sh),MAG);d=ImageDraw.Draw(tile)
  fill=(255,255,255);edge=(199,205,214)
  if caption:fill=ACTIVE;edge=ACTIVE
  if i%4==1:fill=(229,234,240);edge=(184,193,205)
  if i%4==2:fill=(217,229,232);edge=(13,115,119)
  if close and i%4 in (1,2):fill=(232,86,86);edge=fill
  if i%4==3:fill=(244,245,247);edge=(220,224,230)
  d.rounded_rectangle((0,0,w-1,sh-1),radius=4 if not caption else 2,fill=fill,outline=edge,width=1)
  if name=='BUTTON' and i==4:d.rounded_rectangle((0,0,w-1,sh-1),radius=4,outline=(13,115,119),width=1)
  im.paste(tile,(0,i*sh))
 im.save(p)
buttons('BUTTON',5);buttons('CAPTIONBUTTON',8,caption=True);buttons('CLOSEBUTTON',8,caption=True,close=True);buttons('SMALLCLOSEBUTTON',8,caption=True,close=True)
# Flat interior chrome, original procedural artwork. Preserve every atlas size.
def flat(name,color=(247,248,250)):
 p=B/('LIGHT_'+name+'.bmp');Image.new('RGB',Image.open(p).size,color).save(p)
for n in ['TOOLBARBACKGROUND','EXPLORERBARTOOLBARBACKGROUND','SCROLLSHAFTHORIZONTAL','SCROLLSHAFTVERTICAL']:
 flat(n)
for n in ['TOOLBARGRIPPER','TOOLBARGRIPPERVERT','SCROLLTHUMBGRIPPERHORIZONTAL','SCROLLTHUMBGRIPPERVERTICAL']:
 flat(n,MAG)
for n in ['TOOLBARBUTTONS','TOOLBARBUTTONSSPLIT','TOOLBARBUTTONSSPLITDROPDOWN','EXPLORERBARTOOLBARBUTTONS','EXPLORERBARTOOLBARBUTTONSSPLIT','EXPLORERBARTOOLBARBUTTONSSPLITDROPDOWN']:
 p=B/('LIGHT_'+n+'.bmp');w,h=Image.open(p).size;sh=h//6;im=Image.new('RGB',(w,h),MAG);d=ImageDraw.Draw(im)
 for state in [1,2,4,5]:
  color=(231,239,242) if state==1 else (218,237,237)
  d.rounded_rectangle((0,state*sh,w-1,(state+1)*sh-1),radius=3,fill=color)
 im.save(p)
for n,vertical in [('SCROLLTHUMBVERTICAL',True),('SCROLLTHUMBHORIZONTAL',False)]:
 p=B/('LIGHT_'+n+'.bmp');w,h=Image.open(p).size;sh=h//4;im=Image.new('RGB',(w,h),(247,248,250));d=ImageDraw.Draw(im)
 for state,color in enumerate([(151,162,175),(122,135,150),(87,108,125),(210,216,224)]):
  y=state*sh
  box=(w//2-2,y+2,w//2+2,y+sh-3) if vertical else (2,y+sh//2-2,w-3,y+sh//2+2)
  d.rounded_rectangle(box,radius=2,fill=color)
 im.save(p)
def arrow_atlas(name,count=16):
 p=B/('LIGHT_'+name+'.bmp');w,h=Image.open(p).size;sh=h//count;im=Image.new('RGB',(w,h),(247,248,250));d=ImageDraw.Draw(im)
 for state in range(count):
  direction=state//4;cx=w//2;cy=state*sh+sh//2;r=max(2,min(w,sh)//4);col=(47,58,69) if state%4!=3 else (167,176,187)
  coords=[(-r,1),(0,-r+1),(r,1)]
  if direction==1:coords=[(-r,-1),(0,r-1),(r,-1)]
  elif direction==2:coords=[(1,-r),(-r+1,0),(1,r)]
  elif direction==3:coords=[(-1,-r),(r-1,0),(-1,r)]
  d.line([(cx+x,cy+y) for x,y in coords],fill=col,width=1)
 im.save(p)
for n in ['SCROLLARROWS','SCROLLARROWGLYPHS','SCROLLARROWGLYPHSSMALL']:arrow_atlas(n)
p=B/'LIGHT_COMBOBUTTON.bmp';w,h=Image.open(p).size;sh=h//4;im=Image.new('RGB',(w,h),(247,248,250));d=ImageDraw.Draw(im)
for state in range(4):
 d.rounded_rectangle((0,state*sh,w-1,(state+1)*sh-1),radius=3,fill=(255,255,255) if state==0 else (233,240,243),outline=(207,214,222))
im.save(p)
p=B/'LIGHT_COMBOBUTTONGLYPH.bmp';w,h=Image.open(p).size;sh=h//4;im=Image.new('RGB',(w,h),MAG);d=ImageDraw.Draw(im)
for state in range(4):
 cx=w//2;cy=state*sh+sh//2;d.line([(cx-2,cy-1),(cx,cy+1),(cx+2,cy-1)],fill=(47,58,69) if state!=3 else (167,176,187),width=1)
im.save(p)
(OUT/'KUSH-SOURCE.txt').write_text('KushFluent is derived from the Modern theme already shipped in this ReactOS/Kush source tree. Original GPLv3 LICENSE is preserved. Existing controls, glyphs and dark variant retain their original authorship. Light frame and push-button bitmaps are original procedural drawings from tools/theme/gen_kushfluent.py. No Microsoft Windows bitmap, logo or font is included.\n')
for p in (OUT/'lang').glob('*.rc'):
 s=p.read_text().replace('\"Modern\"','\"Kush Fluent\"');p.write_text(s)
print(OUT)
