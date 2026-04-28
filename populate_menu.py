import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from menu.models import Category, MenuItem

# Create categories
categories_data = [
    {'name': 'Appetizers', 'description': 'Start your meal with our delicious appetizers', 'order': 1},
    {'name': 'Main Courses', 'description': 'Hearty and satisfying main dishes', 'order': 2},
    {'name': 'Pizzas', 'description': 'Authentic Italian pizzas baked to perfection', 'order': 3},
    {'name': 'Burgers', 'description': 'Juicy burgers with premium ingredients', 'order': 4},
    {'name': 'Desserts', 'description': 'Sweet endings to your meal', 'order': 5},
    {'name': 'Beverages', 'description': 'Refreshing drinks and beverages', 'order': 6},
]

categories = {}
for cat_data in categories_data:
    cat, _ = Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
    categories[cat.name] = cat

# Create menu items
menu_items_data = [
    # Appetizers
    {'name': 'Bruschetta', 'description': 'Toasted bread topped with fresh tomatoes, basil, and olive oil', 'price': 8.99, 'category': 'Appetizers', 'featured': True},
    {'name': 'Caesar Salad', 'description': 'Crisp romaine lettuce with parmesan, croutons, and Caesar dressing', 'price': 10.99, 'category': 'Appetizers', 'featured': False},
    {'name': 'Garlic Bread', 'description': 'Crispy bread with garlic butter and herbs', 'price': 6.99, 'category': 'Appetizers', 'featured': False},
    {'name': 'Mozzarella Sticks', 'description': 'Golden fried mozzarella with marinara sauce', 'price': 9.99, 'category': 'Appetizers', 'featured': False},
    
    # Main Courses
    {'name': 'Grilled Salmon', 'description': 'Fresh Atlantic salmon with lemon herb butter and seasonal vegetables', 'price': 24.99, 'category': 'Main Courses', 'featured': True},
    {'name': 'Chicken Parmesan', 'description': 'Breaded chicken breast with marinara and melted mozzarella', 'price': 18.99, 'category': 'Main Courses', 'featured': True},
    {'name': 'Ribeye Steak', 'description': '12oz prime ribeye with garlic mashed potatoes and asparagus', 'price': 32.99, 'category': 'Main Courses', 'featured': True},
    {'name': 'Pasta Primavera', 'description': 'Fresh vegetables in garlic olive oil over linguine', 'price': 16.99, 'category': 'Main Courses', 'featured': False},
    
    # Pizzas
    {'name': 'Margherita Pizza', 'description': 'Fresh mozzarella, tomatoes, and basil on classic crust', 'price': 15.99, 'category': 'Pizzas', 'featured': True},
    {'name': 'Pepperoni Pizza', 'description': 'Classic pepperoni with mozzarella and tomato sauce', 'price': 17.99, 'category': 'Pizzas', 'featured': False},
    {'name': 'BBQ Chicken Pizza', 'description': 'Grilled chicken, BBQ sauce, red onions, and cilantro', 'price': 19.99, 'category': 'Pizzas', 'featured': True},
    {'name': 'Veggie Supreme', 'description': 'Bell peppers, mushrooms, olives, onions, and tomatoes', 'price': 16.99, 'category': 'Pizzas', 'featured': False},
    
    # Burgers
    {'name': 'Classic Cheeseburger', 'description': 'Angus beef patty with cheddar, lettuce, tomato, and special sauce', 'price': 13.99, 'category': 'Burgers', 'featured': True},
    {'name': 'Bacon Burger', 'description': 'Topped with crispy bacon, American cheese, and BBQ sauce', 'price': 15.99, 'category': 'Burgers', 'featured': False},
    {'name': 'Mushroom Swiss Burger', 'description': 'Sautéed mushrooms and Swiss cheese on a juicy patty', 'price': 15.99, 'category': 'Burgers', 'featured': False},
    {'name': 'Veggie Burger', 'description': 'Plant-based patty with avocado, lettuce, and tomato', 'price': 14.99, 'category': 'Burgers', 'featured': False},
    
    # Desserts
    {'name': 'Chocolate Lava Cake', 'description': 'Warm chocolate cake with a molten center and vanilla ice cream', 'price': 8.99, 'category': 'Desserts', 'featured': True},
    {'name': 'Tiramisu', 'description': 'Classic Italian dessert with espresso-soaked ladyfingers', 'price': 7.99, 'category': 'Desserts', 'featured': True},
    {'name': 'Cheesecake', 'description': 'New York style cheesecake with berry compote', 'price': 7.99, 'category': 'Desserts', 'featured': False},
    {'name': 'Apple Pie', 'description': 'Warm apple pie with cinnamon and vanilla ice cream', 'price': 6.99, 'category': 'Desserts', 'featured': False},
    
    # Beverages
    {'name': 'Fresh Lemonade', 'description': 'House-made lemonade with fresh lemons', 'price': 3.99, 'category': 'Beverages', 'featured': False},
    {'name': 'Iced Coffee', 'description': 'Cold brew coffee over ice', 'price': 4.99, 'category': 'Beverages', 'featured': False},
    {'name': 'Soft Drinks', 'description': 'Coke, Sprite, or Fanta', 'price': 2.99, 'category': 'Beverages', 'featured': False},
    {'name': 'Sparkling Water', 'description': 'San Pellegrino sparkling water', 'price': 3.99, 'category': 'Beverages', 'featured': False},
]

for item_data in menu_items_data:
    category_name = item_data.pop('category')
    MenuItem.objects.get_or_create(
        name=item_data['name'],
        defaults={
            **item_data,
            'category': categories[category_name]
        }
    )

print("Sample data created successfully!")
print(f"Created {len(categories)} categories and {len(menu_items_data)} menu items")