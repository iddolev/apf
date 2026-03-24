# Concepts & Exploratory Ideas

## More concepts

0
enhance the PRD process

- if there are already existing materials, take from them
- at the end, give it to a "prd reviewer expert" with clean slate, to surface more gaps to inquire
  about

0
Ask the coding expert not to create a code file but first create a list of items,
each item is one element (class, function, global variable), with English description,
starting with the most important elements, i.e. just up to 3 elements, with signature
and no implementation, then implement each separately.
And when implementing one element, immediately check for quality.
Maybe this will ensure better quality.

1
Repeatedly and insistently request feedback and fix (but also detect A->B->A->B->A loop of
changes). Just like I did for the script, kept getting more and more things to fix.
Until reach steady state.

And write to a log ALL the changes - so we can see and improve

2
My approach is: there is GSD, Paul, UltraWork, and many more.
https://www.producthunt.com/products/gstack
So I'm building a pipeline like I think is right +
general purpose ability to tell it:
Inspect framework X and take inspiration from it,
tell me what enhancements we could to do APF based on X's best ideas
if we don't already have them.

3
maybe instruct: do atomic steps, and eac one before you do,
you need to convince the feedbacker and/or devil's advocate why you're doing it
and what's needed, and take into account what they say.
Maybe a "rubber duck" agent that the coder agent talks to

1. TDD test driven design
2. DDD https://claude.ai/chat/717b4a61-741a-4baf-a056-6bac5d31c8e5
3. ADP (acceptance driven programming - Paul?)

## Comments on ulw

1. No consistency between the markdowns of the same agent (e.g. Sysiphus) on different models.
   Some of the differences don't carry meaning. Like this entire thing was generated,
   and the creator didn't make basic checks.
2. It used google-generativeai which is the old unmaintained SDK package (that causes a warning)
   whereas GSD uses the new maintained SDK google-genai.
