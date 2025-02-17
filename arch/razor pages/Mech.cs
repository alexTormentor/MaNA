public class Mech
{
    public string Platform { get; set; }
    public string Engine { get; set; }
    public string Weapon { get; set; }
    public string Body { get; set; }

    public int Durability { get; set; }
    public int Speed { get; set; }
    public int CombatPower { get; set; }

    public Mech(string platform, string engine, string weapon, string body)
    {
        Platform = platform;
        Engine = engine;
        Weapon = weapon;
        Body = body;

        // Расчет характеристик на основе компонентов
        Durability = CalculateDurability(body);
        Speed = CalculateSpeed(platform, engine);
        CombatPower = CalculateCombatPower(weapon);
    }

    private int CalculateDurability(string body)
    {
        return body switch
        {
            "Titanium" => 100,
            "Polys Alloy" => 80,
            _ => 50,
        };
    }

    private int CalculateSpeed(string platform, string engine)
    {
        int baseSpeed = platform switch
        {
            "Strider" => 60,
            "Glider" => 80,
            "Mech" => 40,
            _ => 50,
        };

        int engineBonus = engine switch
        {
            "Quantum" => 30,
            "Nuclear" => 20,
            "Crystal" => 10,
            _ => 0,
        };

        return baseSpeed + engineBonus;
    }

    private int CalculateCombatPower(string weapon)
    {
        return weapon switch
        {
            "Rockets" => 70,
            "Machine Guns" => 50,
            "Flamethrowers" => 60,
            _ => 40,
        };
    }
}