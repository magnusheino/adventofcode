using System;
using System.Linq;

namespace _01_cs
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine(Array.ConvertAll(System.IO.File.ReadAllText("01_input.txt").Split(), int.Parse).Sum());
        }
    }
}
