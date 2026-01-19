import sys
from datetime import date
from storage import append_record, read_all
from analysis import monthly_average, moving_average, month_over_month_change
from viz import plot_bar, ascii_bar_chart

def input_month_year():
    today = date.today()
    y_input = input(f"Year (YYYY) [default {today.year}]: ").strip()
    m_input = input(f"Month (1-12) [default {today.month}]: ").strip()
    year = int(y_input) if y_input else today.year
    month = int(m_input) if m_input else today.month
    if not (1 <= month <= 12):
        raise ValueError("Month must be 1..12")
    return year, month

def input_value():
    val = input("Enter token value (kWh or MWK): ").strip()
    return float(val)

def show_menu():
    print("\n--- Electricity Token Analyzer ---")
    print("1) Add a monthly token value")
    print("2) Show summary statistics")
    print("3) Show ASCII chart")
    print("4) Show plotted chart (matplotlib)")
    print("5) Import sample data")
    print("0) Exit")

def import_sample_data():
    samples = [
        (2024, 9, 120.5),
        (2024,10, 135.8),
        (2024,11, 128.0),
        (2024,12, 140.0),
        (2025,1, 150.2),
        (2025,2, 145.0),
        (2025,3, 155.0),
    ]
    for y,m,v in samples:
        append_record(y,m,v)
    print("Sample data added.")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            try:
                y, m = input_month_year()
                v = input_value()
                append_record(y, m, v)
                print("Saved successfully.")
            except Exception as e:
                print("Error:", e)
        elif choice == "2":
            records = read_all()
            if not records:
                print("No records yet.")
                continue
            avg = monthly_average(records)
            print(f"\nNumber of records: {len(records)}")
            print(f"Overall average: {avg:.2f}")
            ma = moving_average(records, window=3)
            if ma:
                print("3-month moving averages:")
                for i, mv in enumerate(ma, start=1):
                    print(f"  window {i}: {mv:.2f}")
            changes = month_over_month_change(records)
            if changes:
                print("Month-over-month % changes:")
                for i, ch in enumerate(changes, start=1):
                    print(f"  {i} -> {i+1}: {ch:.2f}%")
        elif choice == "3":
            ascii_bar_chart(read_all())
        elif choice == "4":
            plot_bar(read_all())
        elif choice == "5":
            import_sample_data()
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
