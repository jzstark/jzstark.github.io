---
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

#layout: home
layout: page
#title: Home
---

<img src="/images/stark.jpg" style="float:right;width:200px;margin-left:20px">

I am a Post-doc working at the Beijing Institute of Technology. I acquired my PhD at the [Computer Laboratory](https://www.cl.cam.ac.uk/), University of Cambridge (affiliated with Corpus Christi College), supervised by [Professor Jon Crowcroft](https://www.cl.cam.ac.uk/~jac22/). 

I am interested in various research topics, including numerical computation, high performance computing, machine learning, and their application in the real world. 
I have been actively participating in the development of [Owl](https://ocaml.xyz/), a scientific computing library that is widely used in the [OCaml](https://ocaml.org) community, as a main developer. Currently I focus on developing a [symbolic](https://github.com/owlbarn/owl_symbolic) library based on Owl, and leading Owl's [tutorial book](https://ocaml.xyz/book/).

I am always glad to face new challenges. I have been practising Kendo in the [University of Cambridge Kendo Society](http://kendo.soc.srcf.net/) for three years. 
I have also participated in the [STIMULUS programme](https://stimulus.maths.org/) as volunteer to assist teaching computer science to pupils in local schools.

Test for Code format:

```ocaml
# let f opt = match opt with
    | None -> None
    | Some None -> None
    | Some (Some x) -> Some x;;
val f : 'a option option-> 'a option = <fun>
```


```c
#include <stdio.h>
int main() {
   int year;
   printf("Enter a year: ");
   scanf("%d", &year);

   // leap year if perfectly divisible by 400
   if (year % 400 == 0) {
      printf("%d is a leap year.", year);
   }
   // not a leap year if divisible by 100
   // but not divisible by 400
   else if (year % 100 == 0) {
      printf("%d is not a leap year.", year);
   }
   // leap year if not divisible by 100
   // but divisible by 4
   else if (year % 4 == 0) {
      printf("%d is a leap year.", year);
   }
   // all other years are not leap years
   else {
      printf("%d is not a leap year.", year);
   }

   return 0;
}
```