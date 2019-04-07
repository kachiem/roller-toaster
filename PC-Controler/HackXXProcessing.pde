//import class to set up serial connection with wiring board
import processing.serial.*;
Serial port;
//button setup
color currentcolor;
RectButton UpButton, DownButton, LeftButton, RightButton, survoLeftButton, survoRightButton;
boolean locked = false;
 
void setup() {
   //set up window
   size(600, 200);
   color baseColor = color(102, 102, 102);

   // List all the available serial ports in the output pane.
   // You will need to choose the port that the Wiring board is
   // connected to from this list. The first port in the list is
   // port #0 and the third port in the list is port #2.
   println(Serial.list());
   // Open the port that the Wiring board is connected to (in this case 1
   // which is the second open port in the array)
   // Make sure to open the port at the same speed Wiring is using (9600bps)
   port = new Serial(this, Serial.list()[2], 115200);
   // Define and create rectangle button #1
   int x = 30;
   int y = 100;
   int size = 50;
   color buttoncolor = color(153, 102, 102);
   color highlight = color(102, 51, 51);
   UpButton = new RectButton(x, y, size, buttoncolor, highlight);
   // Define and create rectangle button #2
   x = 90;
   y = 100;
   DownButton = new RectButton(x, y, size, buttoncolor, highlight);
   x = 150;
   y = 100;
   LeftButton = new RectButton(x, y, size, buttoncolor, highlight);
   x = 210;
   y = 100;
   RightButton = new RectButton(x, y, size, buttoncolor, highlight);
}
 
void draw() {
   background(color(102, 102, 102));
   stroke(255);
   update(mouseX, mouseY);
   UpButton.display();
   DownButton.display();
   LeftButton.display();
   RightButton.display();
}
 
void update(int x, int y) {
   if(locked == false) {
      UpButton.update();
      DownButton.update();
      LeftButton.update();
      RightButton.update();
   } else {
      locked = false;
   }
   //Turn LED on and off if buttons pressed where
   //H = on (high) and L = off (low)
   if(mousePressed) {
      if(UpButton.pressed()) { //UP button
         port.write('w');
         print("Up ");
         delay(450);
      } else if(DownButton.pressed()) { //DOWN button
         port.write('s');
         print("Down ");
         delay(450);
      } else if(LeftButton.pressed()){
         port.write('a');
         print("Left ");
         delay(300);
      } else if(RightButton.pressed()){
        port.write('d');
        print("Right ");
        delay(300);
      }
      
   }
}
 
 
class Button {
   int x, y;
   int size;
   color basecolor, highlightcolor;
   color currentcolor;
   boolean over = false;
   boolean pressed = false;
   void update() {
      if(over()) {
         currentcolor = highlightcolor;
      } else {
         currentcolor = basecolor;
      }
   }
   boolean pressed() {
      if(over) {
          locked = true;
          return true;
      } else {
          locked = false;
          return false;
      }
   }
   boolean over() {
      return true;
   }
   void display() {
   }
}
 
class RectButton extends Button {
   RectButton(int ix, int iy, int isize, color icolor, color ihighlight) {
      x = ix;
      y = iy;
      size = isize;
      basecolor = icolor;
      highlightcolor = ihighlight;
      currentcolor = basecolor;
   }
   boolean over() {
      if( overRect(x, y, size, size) ) {
         over = true;
         return true;
       } else {
         over = false;
         return false;
       }
    }
   void display() {
      stroke(255);
      fill(currentcolor);
      rect(x, y, size, size);
   }
}
 
boolean overRect(int x, int y, int width, int height) {
   if (mouseX >= x && mouseX <= x+width && mouseY >= y && mouseY <= y+height) {
      return true;
   } else {
      return false;
   }
}
