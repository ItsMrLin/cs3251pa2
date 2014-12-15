A New Reliable Transport Protocol
============================

authors: Zhiyuan "Jerry" Lin and Pavleen Thukral

This is a reliable transport protocol written and designed from the ground up. By processing through UPD packets we are able to write our own transport protocol to handle reliable transport better than TCP. 

Our design specification is detailed here https://docs.google.com/document/d/1dlTbf-VROXj3FJv5s3wbI66oF3urJvpKLCoxEq4cJCk/edit?usp=sharing

This code was written for a class project, but we are very proud of the improvements we've made. 

This code is not 100% bug free. Feel free to contribute and improve!


Usage
=====
There are two set of client server examples provided in the code. 

- The first set is fta-client.py and fta-server.py. These files work with the the NetEmu package included in this repository. This package has a readme included.
- The second set is test.py and clientTest.py. These are very self explanitory and simple. Just look at the code. 
