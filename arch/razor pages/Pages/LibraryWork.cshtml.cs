using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System;
using System.Collections.Generic;
using System.Linq;

namespace MechsRazorPages.Pages
{
    public class LibraryWorkModel : PageModel
    {
        private readonly Library _library = new Library();

        public List<Book> Books { get; set; } = new List<Book>();
        public List<string> Genres { get; set; } = new List<string>();
        public List<string> Settings { get; set; } = new List<string>();
        
        [BindProperty(SupportsGet = true)]
        public string SelectedGenre { get; set; }
        
        [BindProperty(SupportsGet = true)]
        public string SelectedSetting { get; set; }

        public void OnGet()
        {
            Books = _library.LoadBooks();

            Genres = Books.Select(b => b.Genre).Distinct().ToList();
            Settings = Books.Select(b => b.Setting).Distinct().ToList();

            // Применяем фильтры, если они указаны
            if (!string.IsNullOrEmpty(SelectedGenre))
            {
                Books = Books.Where(b => b.Genre.Equals(SelectedGenre, StringComparison.OrdinalIgnoreCase)).ToList();
            }

            if (!string.IsNullOrEmpty(SelectedSetting))
            {
                Books = Books.Where(b => b.Setting.Equals(SelectedSetting, StringComparison.OrdinalIgnoreCase)).ToList();
            }
        }
    }
}