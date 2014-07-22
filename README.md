Wortmaschine
============

Quick reimplementation of an old just-for-fun word generation program. Inspired
by my German friend's admission that I spoke the best fake German he'd ever
heard, and a desire to learn a little linguistics and extend that ability to any
language. Mostly it's just fun to look at funny words, a list of which may be
found in favorite-words.md.

Currently BYOC (Bring Your Own Corpus) — check out [Street-Smart Language
Learning][] or [Wiktionary][] for some quick and easy-to-use word lists, or the
[American National Corpus][] if you're super hardcore and want to do your own
advanced analysis.

All code is in a single module, so just import it and look at the `if __name__
== '__main__'` block for a usage example.

Some friends and I have also experimented with applying these principles to text
body generation, and ended up producing a [Red Hot Chili Peppers B-Sides album
maker][RHCP].

[Street-Smart Language Learning]: http://www.streetsmartlanguagelearning.com/2008/12/top-10000-words-in-dutch-english-french.html
[Wiktionary]: http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists
[American National Corpus]: http://www.americannationalcorpus.org/
[RHCP]: https://bitbucket.org/morganrobertson/textfun
