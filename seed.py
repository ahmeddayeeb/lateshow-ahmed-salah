from app import app, db, Episode, Guest, Appearance
import csv

def seed_database():
    with app.app_context():
        # Clear existing data
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        db.session.commit()

        # Read data from CSV file
        csv_file = 'seed_data.csv'
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                year = row['YEAR']
                occupation_show = row['GoogleKnowlege_OccupationShow']
                date = row['Group']
                raw_guest_list = row['Raw_Guest_List']

                # Create Episode
                episode = Episode(date=date, number=year)
                db.session.add(episode)
                db.session.commit()

                # Create Guest
                guest = Guest(name=raw_guest_list, occupation=occupation_show)
                db.session.add(guest)
                db.session.commit()

                # Create Appearance
                appearance = Appearance(rating=5, guest_id=guest.id, episode_id=episode.id)
                db.session.add(appearance)

        db.session.commit()
        print('Database seeded successfully!')

if __name__ == '__main__':
    seed_database()
