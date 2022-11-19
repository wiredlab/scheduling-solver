# Notes

Init `git` repository to track changes.

Create `requirements.txt` for installing required packages with `pip`.

Install packages into a virtual environment.  `pip install -r requirements.txt`

Add extra package `openpyxl` needed to read XLSX files.


Run `python schedulingLP.py`, output is:

```
Decision Variable/Allocation Matrix: 

[[X_010 X_011 X_012 X_013 X_014 X_015 X_016 X_017 X_018 X_019 X_020 X_021
  X_022 X_023 X_024 X_025 X_026 X_027 X_028 X_029 X_030]
 [X_110 X_111 X_112 X_113 X_114 X_115 X_116 X_117 X_118 X_119 X_120 X_121
  X_122 X_123 X_124 X_125 X_126 X_127 X_128 X_129 X_130]
 [X_210 X_211 X_212 X_213 X_214 X_215 X_216 X_217 X_218 X_219 X_220 X_221
  X_222 X_223 X_224 X_225 X_226 X_227 X_228 X_229 X_230]
 [X_310 X_311 X_312 X_313 X_314 X_315 X_316 X_317 X_318 X_319 X_320 X_321
  X_322 X_323 X_324 X_325 X_326 X_327 X_328 X_329 X_330]
 [X_410 X_411 X_412 X_413 X_414 X_415 X_416 X_417 X_418 X_419 X_420 X_421
  X_422 X_423 X_424 X_425 X_426 X_427 X_428 X_429 X_430]
 [X_510 X_511 X_512 X_513 X_514 X_515 X_516 X_517 X_518 X_519 X_520 X_521
  X_522 X_523 X_524 X_525 X_526 X_527 X_528 X_529 X_530]
 [X_610 X_611 X_612 X_613 X_614 X_615 X_616 X_617 X_618 X_619 X_620 X_621
  X_622 X_623 X_624 X_625 X_626 X_627 X_628 X_629 X_630]
 [X_710 X_711 X_712 X_713 X_714 X_715 X_716 X_717 X_718 X_719 X_720 X_721
  X_722 X_723 X_724 X_725 X_726 X_727 X_728 X_729 X_730]]


X_010 + X_110 + X_210 + X_310 + X_410 + X_510 + X_610 + X_710 = 2
X_011 + X_111 + X_211 + X_311 + X_411 + X_511 + X_611 + X_711 = 2
X_012 + X_112 + X_212 + X_312 + X_412 + X_512 + X_612 + X_712 = 1
X_013 + X_113 + X_213 + X_313 + X_413 + X_513 + X_613 + X_713 = 1
X_014 + X_114 + X_214 + X_314 + X_414 + X_514 + X_614 + X_714 = 1
X_015 + X_115 + X_215 + X_315 + X_415 + X_515 + X_615 + X_715 = 1
X_016 + X_116 + X_216 + X_316 + X_416 + X_516 + X_616 + X_716 = 1
X_017 + X_117 + X_217 + X_317 + X_417 + X_517 + X_617 + X_717 = 1
X_018 + X_118 + X_218 + X_318 + X_418 + X_518 + X_618 + X_718 = 1
X_019 + X_119 + X_219 + X_319 + X_419 + X_519 + X_619 + X_719 = 1
X_020 + X_120 + X_220 + X_320 + X_420 + X_520 + X_620 + X_720 = 1
X_021 + X_121 + X_221 + X_321 + X_421 + X_521 + X_621 + X_721 = 1
X_022 + X_122 + X_222 + X_322 + X_422 + X_522 + X_622 + X_722 = 1
X_023 + X_123 + X_223 + X_323 + X_423 + X_523 + X_623 + X_723 = 1
X_024 + X_124 + X_224 + X_324 + X_424 + X_524 + X_624 + X_724 = 1
X_025 + X_125 + X_225 + X_325 + X_425 + X_525 + X_625 + X_725 = 1
X_026 + X_126 + X_226 + X_326 + X_426 + X_526 + X_626 + X_726 = 1
X_027 + X_127 + X_227 + X_327 + X_427 + X_527 + X_627 + X_727 = 1
X_028 + X_128 + X_228 + X_328 + X_428 + X_528 + X_628 + X_728 = 2
X_029 + X_129 + X_229 + X_329 + X_429 + X_529 + X_629 + X_729 = 3
Traceback (most recent call last):
  File "schedulingLP.py", line 73, in <module>
    print(lpSum(allocation[i][j] for i in range(n_profs)) == course_needs[j])
  File "/home/dan/tmp/sami-scheduling/.direnv/python-3.8.10/lib/python3.8/site-packages/pulp/pulp.py", line 1028, in __eq__
    return LpConstraint(self - other, const.LpConstraintEQ)
  File "/home/dan/tmp/sami-scheduling/.direnv/python-3.8.10/lib/python3.8/site-packages/pulp/pulp.py", line 943, in __sub__
    return self.copy().subInPlace(other)
  File "/home/dan/tmp/sami-scheduling/.direnv/python-3.8.10/lib/python3.8/site-packages/pulp/pulp.py", line 918, in subInPlace
    self.subInPlace(e)
  File "/home/dan/tmp/sami-scheduling/.direnv/python-3.8.10/lib/python3.8/site-packages/pulp/pulp.py", line 918, in subInPlace
    self.subInPlace(e)
  File "/home/dan/tmp/sami-scheduling/.direnv/python-3.8.10/lib/python3.8/site-packages/pulp/pulp.py", line 918, in subInPlace
    self.subInPlace(e)
  [Previous line repeated 987 more times]
  File "/home/dan/tmp/sami-scheduling/.direnv/python-3.8.10/lib/python3.8/site-packages/pulp/pulp.py", line 916, in subInPlace
    elif isinstance(other, list) or isinstance(other, Iterable):
  File "/usr/lib/python3.8/abc.py", line 98, in __instancecheck__
    return _abc_instancecheck(cls, instance)
RecursionError: maximum recursion depth exceeded in comparison
```



Ok.... maybe my system version of python (3.8) is a little old.
Switch to using `conda` to manage environments and use python3.11

Capture packages installed in the conda environment in `environment.yml`


