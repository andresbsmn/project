
#include "Buig_Driver.h"
bool hoog = false;
bool midden = false;
bool laag = false;
void buigsensor(){
  
  int flexValue = analogRead(pinFlex);
  if(flexValue>1010){
    hoog = true;
  }
  else if(flexValue > 700){
    midden = true;
  }
  else if(flexValue<400){
    laag = true;
  }

  if(hoog && midden && laag){
    Keyboard.press('k');
    hoog =false;
    midden = false;
    laag = false;
    Keyboard.release('k');
  }

}
