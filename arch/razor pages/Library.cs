using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace MechsRazorPages
{
    public class Library
    {
        private readonly string _dbPath = "DB/BookData.json";

        public List<Book> LoadBooks()
        {
            var filePath = Path.Combine(Directory.GetCurrentDirectory(), _dbPath);

            if (!File.Exists(filePath))
            {
                Console.WriteLine("JSON file not found at path: " + filePath);
                return new List<Book>();
            }

            var jsonData = File.ReadAllText(filePath);
            return JsonConvert.DeserializeObject<List<Book>>(jsonData) ?? new List<Book>();
        }
    }

    public class Book
    {
        public string Title { get; set; }
        public string Author { get; set; }
        public string Genre { get; set; }
        public string Setting { get; set; }
        public double Rating { get; set; }
        public double Price { get; set; }
        public DateTime ReleaseDate { get; set; }
    }
}