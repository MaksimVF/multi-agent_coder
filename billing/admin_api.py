



from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base, TariffPlan, TariffComponent, tariff_components

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///billing_admin.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/api/v1/admin/tariffs', methods=['POST'])
def create_tariff():
    """
    Create a new tariff plan
    """
    data = request.json
    session = Session()

    try:
        # Create tariff plan
        tariff = TariffPlan(
            name=data['name'],
            description=data.get('description', ''),
            price_per_month=data['price_per_month'],
            included_credits=data.get('included_credits', 0),
            max_team_members=data.get('max_team_members', 1),
            member_price=data.get('member_price', 0),
            discounts=data.get('discounts', {})
        )
        session.add(tariff)
        session.commit()

        # Add components
        for component_data in data.get('components', []):
            component = session.query(TariffComponent).get(component_data['id'])
            if component:
                tariff.components.append(component)
                # Set included units
                session.execute(
                    tariff_components.insert().values(
                        tariff_id=tariff.id,
                        component_id=component.id,
                        included_units=component_data.get('included_units', 0)
                    )
                )

        session.commit()

        return jsonify({
            "message": "Tariff created successfully",
            "tariff_id": tariff.id
        })

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route('/api/v1/admin/components', methods=['POST'])
def create_component():
    """
    Create a new tariff component
    """
    data = request.json
    session = Session()

    try:
        component = TariffComponent(
            name=data['name'],
            description=data.get('description', ''),
            unit_type=data['unit_type'],
            price_per_unit=data['price_per_unit'],
            is_premium=data.get('is_premium', False),
            is_exclusive=data.get('is_exclusive', False),
            exclusive_tariffs=data.get('exclusive_tariffs', [])
        )
        session.add(component)
        session.commit()

        return jsonify({
            "message": "Component created successfully",
            "component_id": component.id
        })

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True, port=5001)



