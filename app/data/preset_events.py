from datetime import datetime, timedelta
from app.models.schemas import (
    EventIntakeRequest,
    EventCategory,
    ExperienceTier,
    PriorityRanking,
    DigitalInvitationTheme,
    CeremonyScheduleItem,
)

def _get_future_date_str(days_ahead: int) -> str:
    return (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

PRESET_EVENTS = {
    "wedding_srinivas_scenario": {
        "label": "The Royal Vivah (SME Video Benchmark: 200 Guests, ₹8L Budget)",
        "intake": EventIntakeRequest(
            title="Saurav & Saumya Royal Vivah & Reception",
            category=EventCategory.WEDDING,
            guest_count=200,
            total_budget=800000.0,
            target_date=_get_future_date_str(120),
            location_city="Devbhoomi & Delhi NCR",
            experience_tier=ExperienceTier.STANDARD,
            priority_weights=PriorityRanking(catering=1, venue=2, decor=3, photography=4, entertainment=5),
            must_haves=[
                "Organic Himalayan Pahadi Food Counter",
                "Heritage Mandap with Brass Oil Lamps",
                "Live Sitar & Shehnai Welcoming Ensemble",
                "High-Speed Interactive Digital Invitation Suite",
            ],
            special_notes="Focus deeply on culinary hospitality and warm cultural ambiance rather than sterile luxury.",
        ),
        "theme": DigitalInvitationTheme(
            theme_name="Devbhoomi Royal Heritage & Pastel Gold",
            aesthetic_style="Regal Indian Heritage with Contemporary Glassmorphism",
            palette={
                "primary": "#b38034",    # Royal Antique Gold
                "secondary": "#2b1c10",  # Rich Deep Walnut
                "accent": "#e07a5f",     # Warm Terracotta
                "background": "#0f0e0c", # Midnight Onyx
                "card_bg": "#1c1917",    # Deep Umber Card
            },
            typography_heading="'Playfair Display', serif",
            typography_body="'Outfit', sans-serif",
            ambient_audio_track="artful_wedding_theme.mp3",
            rsvp_link_slug="saurav-weds-saumya",
            ceremonies=[
                CeremonyScheduleItem(
                    ceremony_name="Shubh Haldi Carnival",
                    date_label="Day 1 • Morning 10:30 AM",
                    time_window="10:30 AM - 1:30 PM",
                    venue_type="Sunlit Courtyard Lawn",
                    dress_code="Sunny Yellows & Traditional Florals",
                    music_vibe="Folk Dholak & Upbeat Festive Acoustics",
                    key_highlights=["Organic turmeric rituals", "Fresh sugarcane juice bar", "Phoolon ki Holi"],
                ),
                CeremonyScheduleItem(
                    ceremony_name="Mehendi & Sangeet Soirée",
                    date_label="Day 1 • Evening 6:00 PM",
                    time_window="6:00 PM - 11:30 PM",
                    venue_type="Illuminated Grand Amphitheatre",
                    dress_code="Emerald Greens & Shimmering Lehengas",
                    music_vibe="Live Fusion Band & Retro Bollywood Beats",
                    key_highlights=["Artisanal henna artists", "Chaat street banquet", "Choreographed family dance battle"],
                ),
                CeremonyScheduleItem(
                    ceremony_name="Shubh Vivah & Vedic Pheras",
                    date_label="Day 2 • Evening 5:00 PM",
                    time_window="5:00 PM - 9:00 PM",
                    venue_type="Royal Heritage Glass Mandap",
                    dress_code="Royal Ivory & Crimson Red",
                    music_vibe="Sacred Vedic Chants & Classical Shehnai",
                    key_highlights=["Baraat with Brass Band", "Varmala under cold fireworks", "Traditional 7 Pheras"],
                ),
                CeremonyScheduleItem(
                    ceremony_name="Grand Reception Banquet",
                    date_label="Day 2 • Night 9:00 PM",
                    time_window="9:00 PM - Midnight",
                    venue_type="Crystal Grand Ballroom",
                    dress_code="Black Tie & Regal Evening Formals",
                    music_vibe="Symphonic Strings & Lounge Jazz",
                    key_highlights=["Gourmet 8-course banquet", "Cake cutting ceremony", "Thank you photo desk"],
                ),
            ],
        ),
    },
    "tech_community_gala": {
        "label": "GenAI Tech Summit & Developers Gala (350 Attendees, ₹4L Budget)",
        "intake": EventIntakeRequest(
            title="PromptWars India Developers Summit & Awards Gala",
            category=EventCategory.COMMUNITY_GALA,
            guest_count=350,
            total_budget=400000.0,
            target_date=_get_future_date_str(45),
            location_city="Bengaluru / Gurugram",
            experience_tier=ExperienceTier.STANDARD,
            priority_weights=PriorityRanking(catering=2, venue=1, decor=4, photography=3, entertainment=5),
            must_haves=[
                "Dual High-Lumen Projector Screens & 1000Mbps Fiber WiFi",
                "Continuous Espresso & High-Protein Snack Station",
                "Live Video Stream & Social Media Photo Booth",
            ],
            special_notes="Prioritize rock-solid audio-visual gear, seating power sockets, and networking zone flow.",
        ),
        "theme": DigitalInvitationTheme(
            theme_name="Cybernetic Google Neon",
            aesthetic_style="Ultra-Modern Dark Mode with Neon Cyan & Emerald Accents",
            palette={
                "primary": "#4285f4",
                "secondary": "#34a853",
                "accent": "#fbbc05",
                "background": "#0b0f19",
                "card_bg": "#151d2f",
            },
            typography_heading="'Space Grotesk', sans-serif",
            typography_body="'Inter', sans-serif",
            ambient_audio_track="ambient_synthwave.mp3",
            rsvp_link_slug="promptwars-summit-2026",
            ceremonies=[
                CeremonyScheduleItem(
                    ceremony_name="Keynote & Architectural Lightning Talks",
                    date_label="Day 1 • 9:30 AM",
                    time_window="9:30 AM - 1:00 PM",
                    venue_type="Main Auditorium",
                    dress_code="Smart Casuals / Tech Tees",
                    music_vibe="Lo-Fi Coding Beats",
                    key_highlights=["Keynote address", "Live GenAI demos", "Swag bag distribution"],
                ),
                CeremonyScheduleItem(
                    ceremony_name="Hackathon Finals & Swag Awards Ceremony",
                    date_label="Day 1 • 4:00 PM",
                    time_window="4:00 PM - 8:30 PM",
                    venue_type="Exhibition Hall & Networking Lounge",
                    dress_code="Smart Casuals",
                    music_vibe="High-Energy Electronic Synth",
                    key_highlights=["Top 10 Demos", "Trophy presentation", "Networking dinner & cocktails"],
                ),
            ],
        ),
    },
    "golden_jubilee_birthday": {
        "label": "Golden Jubilee 50th Birthday Carnival (80 Guests, ₹1.8L Budget)",
        "intake": EventIntakeRequest(
            title="Dr. Rajesh 50th Golden Jubilee Birthday Carnival",
            category=EventCategory.BIRTHDAY,
            guest_count=80,
            total_budget=180000.0,
            target_date=_get_future_date_str(21),
            location_city="Dehradun",
            experience_tier=ExperienceTier.PREMIUM_LUXURY,
            priority_weights=PriorityRanking(catering=1, venue=3, decor=2, photography=4, entertainment=5),
            must_haves=[
                "Custom 3-Tier Pistachio Belgian Chocolate Cake",
                "Retro 80s Live Bollywood Karaoke Singer",
                "Memory Lane Photo Tunnel spanning 5 Decades",
            ],
            special_notes="Intimate family gathering with elderly guests; ensure comfortable indoor seating and ramp access.",
        ),
        "theme": DigitalInvitationTheme(
            theme_name="Vintage Golden Twilight",
            aesthetic_style="Warm Art-Deco Gold with Velvet Navy",
            palette={
                "primary": "#d4af37",
                "secondary": "#1a2238",
                "accent": "#98d7c2",
                "background": "#0e131f",
                "card_bg": "#171f33",
            },
            typography_heading="'Cinzel', serif",
            typography_body="'Montserrat', sans-serif",
            ambient_audio_track="golden_jubilee_waltz.mp3",
            rsvp_link_slug="rajesh-turns-50",
            ceremonies=[
                CeremonyScheduleItem(
                    ceremony_name="Memory Lane High Tea & Welcome",
                    date_label="Evening • 5:00 PM",
                    time_window="5:00 PM - 6:30 PM",
                    venue_type="Boutique Tea Garden Lounge",
                    dress_code="Semi-Formal Pastels",
                    music_vibe="Retro Vinyl 70s-80s Melodies",
                    key_highlights=["5-decade photo tunnel", "Gourmet tea tasting", "Storytelling circle"],
                ),
                CeremonyScheduleItem(
                    ceremony_name="Jubilee Cake Cutting & Gala Dinner",
                    date_label="Night • 7:30 PM",
                    time_window="7:30 PM - 11:00 PM",
                    venue_type="Fireplace Dining Hall",
                    dress_code="Evening Elegance",
                    music_vibe="Live Acoustic Ghazals & Retro Bollywood",
                    key_highlights=["Grand cake cutting", "Family video tribute", "Chefs table live dinner"],
                ),
            ],
        ),
    },
}

def get_preset_event(preset_key: str):
    return PRESET_EVENTS.get(preset_key, PRESET_EVENTS["wedding_srinivas_scenario"])
