''' @file                       mainpage.py
    @author                     Jeremy Baechler
    @author                     Kendall Chappell
    @author                     Matthew Wimberley
    @date                       24-Feb-2022
    
    @brief                      This develops the main page of our term project portfolio
    @details                    Using doxywizard we are able to compile our entire website
                                using special documentation formatting our repository.
                                
    @page    Design             SCARA Robot Design
    
    @section sec_intro          Software Design
                                To make our lives easier we plan on using the program Inkscape
                                to convert our images into HPGL files. With these files we can 
                                grab the x and y coordinates for our plot and use our subsequent
                                analysis to derive the arm angles needed for our desired 
                                coordinates.
                                
                                We will use inverse kinematics we learned from ME 423 to get the 
                                necessary angles such that our end effector is at our coordinate. 
                                The PID controller will take these new coordinates and compute an 
                                appropriate motor duty cycle so that our motors spin to the right
                                set point. The encoder then passes the current position along to our
                                position checker and our controller to complete the closed loop.      
                                
                                
    @subsection Tasks           Task Diagram
   
    @image                      html    SCARA_Task_Diagram-1.png    "SCARA Robot Task Diagram"  width = 800px 
    
    @subsection FSM             Finite State Machine Diagrams
    
    @image                      html    User_Task_FSM-1.png           "User Task FSM"  width = 800px
    
    @image                      html    Position_Check_Task_FSM-1.png "Position Check Task FSM"  width = 800px
    
    @image                      html    Encoder_Task_FSM-1.png        "Encoder Task FSM"  width = 800px
    
    @image                      html    Controller_Task_FSM-1.png     "Controller Task FSM"  width = 800px
    
    @image                      html    Motor_Task_FSM-1.png          "Motor Task FSM"  width = 800px
'''                         