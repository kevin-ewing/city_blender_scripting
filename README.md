# City Blender Scripting

This is a small collection of the work I have done in my spring 2022 semester in my Animation Studio Independent study. This semester I tasked myself with independently learning blenders python API, and exploring generative/procedural art. This was my first project. I hope you enjoy the artwork either the sample renders or by exploring the generation yourself.

---

## Installation
With the github CLI:

```bash
gh repo clone kevin-ewing/city_blender_scripting
```

With http:
```bash
git clone https://github.com/kevin-ewing/city_blender_scripting.git
```

---

## Usage

`run.sh` has two ways of being run. One with a single render and another that loops through and renders many images. For one output:
```bash
$ ./run.sh {single_output_number}
```
For example:
```bash
$ ./run.sh 23
```

For a sequence of output renders use:

```bash
$ ./run.sh {output_start_number} {output_end_number}
```
For example:
```bash
$ ./run.sh 1 50
```
The rendered image files will be output to ./output/output_{output_number}.png

---

## Sample Outputs
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_1.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_2.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_3.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_4.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_5.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_6.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_7.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_8.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_9.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_10.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_11.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_12.png?raw=true)
![alt output](https://github.com/kevin-ewing/city_blender_scripting/blob/master/sample_output/output_13.png?raw=true)

---
## License
MIT License

Copyright (c) 2022 Kevin Ewing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.