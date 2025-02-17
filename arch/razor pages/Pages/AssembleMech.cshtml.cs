using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace MechsRazorPages.Pages
{
    public class AssembleMechModel : PageModel
    {
        [BindProperty]
        public string Platform { get; set; }

        [BindProperty]
        public string Engine { get; set; }

        [BindProperty]
        public string Weapon { get; set; }

        [BindProperty]
        public string Body { get; set; }

        public Mech AssembledMech { get; set; }

        public void OnPost()
        {
            AssembledMech = new Mech(Platform, Engine, Weapon, Body);
        }
    }
}