.. |date| date::

=============================
How to overengineer a website
=============================

I have tried to get into web development a lot, but in order to avoid dying early of an anger-induced heart attack, I have to keep staying away from
it.

But I kind of talked about why I wanted my own website in the `home page </index.html>`__, and I decided to put together a static website just *once*
so I could get it over with. This instead resulted in a long-winded journey of writing automations just to avoid touching Javascript.

Sure, it would *probably* have been easier to just write a HTML page and style it. But scalability is a big deal if I want to be able to add content
without getting bogged down with individually considering the structure of each page.

Also, using an existing tool like `WordPress <https://wordpress.com/>`__ *would* make sense to an intelligent person, which is why I didn't.

So, with my justification (copium) out of the way, my main ambitions for this project were:

1. Maximise accessibility and device/browser support (mostly by keeping to `HTML standards <https://html.spec.whatwg.org/multipage/>`__)
2. Prioritise navigation and usability over looks
3. Make it as easy as possible to add content so the time spent writing the build pipeline is worth it

I won't discuss the first two since there's not much to be said, but I figure documenting my solution to the third rule might be of use to anyone
else with the same goals.

.. ...............................
.. footer:: Last edited on |date|.
