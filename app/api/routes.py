from flask import Blueprint, jsonify, request, abort
from .models import setup_db, Trail, Region, Review
from uuid import uuid4, UUID
import json
from .auth import AuthError, requires_auth

api = Blueprint('api', __name__, url_prefix='/api')

ITEMS_PER_PAGE = 10

def paginate_items(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * ITEMS_PER_PAGE
  end = start + ITEMS_PER_PAGE

  items = [item.format() for item in selection]
  current_items = items[start:end]

  return current_items

#GET Regions
@api.route('/regions')
def get_regions():
  try:
    regions = Region.query.all()
    regions_list = paginate_items(request, regions)
    #regions_list = [region.format() for region in regions]

    if len(regions_list) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'total_regions': len(regions_list),
      'regions': regions_list
    }), 200
  except Exception as error:
    print(error)
    return jsonify({
      'success': False,
      'error': str(error)
    }), 500

#POST Regions
@api.route('/regions', methods=['POST'])
@requires_auth('post:regions')
def add_regions(payload):
  data = request.get_json()

  name = data.get('name', None)
  reg_type = data.get('reg_type', None)

  try:
    new_region = Region(name=name, reg_type=reg_type)
    new_region.insert()

    return jsonify({
      'success': True,
      'created': new_region.id,
      'total_regions': len(Region.query.all())
    })
  except Exception as error:
    abort(error.code)

#DELETE Regions
@api.route('/regions/<int:region_id>', methods=['DELETE'])
@requires_auth('delete:regions')
def delete_region(payload, region_id):
  region = Region.query.get_or_404(region_id)

  if region:
    try:
      region.delete()
      return jsonify({
        'success': True,
        'deleted': region_id,
        'total_regions': len(Region.query.all())
      })
    except Exception as error:
      abort(error.code)

#PATCH Regions
@api.route('regions/<int:region_id>', methods=['PATCH'])
@requires_auth('patch:regions')
def update_region(payload, region_id):
  region = Region.query.get_or_404(region_id)

  if region:
    try:
      data = request.get_json()
      name = data.get('name', None)
      reg_type = data.get('reg_type', None)

      if not data:
        abort(400)
      if name:
        region.name = name
      if reg_type:
        region.reg_type = reg_type
      
      region.update()

      return jsonify({
        'success': True,
        'region': [region.format()]
      }), 200
    except Exception as error:
      abort(error.code)

#GET Trails
@api.route('/trails')
def get_trails():
  try:
    trails = Trail.query.all()
    trails_list = paginate_items(request, trails)

    if len(trails_list) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'total_trails': len(trails_list),
      'trails': trails_list
    }), 200
  except Exception as error:
    print(error)
    return jsonify({
      'success': False,
      'error': str(error)
    }), 500

#POST Trails
@api.route('/trails', methods=['POST'])
@requires_auth('post:trails')
def add_trails(payload):
  body = request.get_json()

  name = body.get('name', None)
  distance = body.get('distance', None)
  elevation = body.get('elevation', None)
  difficulty = body.get('difficulty', None)
  coordination = body.get('coordination', None)
  parking = body.get('parking', None)

  try:
    new_trail = Trail(
      name=name,
      distance=distance,
      elevation=elevation,
      difficulty=difficulty,
      coordination=json.dumps(coordination),
      parking=parking
      )
    new_trail.insert()

    return jsonify({
      'success': True,
      'created': new_trail.id,
      'total_trails': len(Trail.query.all())
    })
  except Exception as error:
    abort(error.code)

#DELETE Trails
@api.route('/trails/<int:trail_id>', methods=['DELETE'])
@requires_auth('delete:trails')
def delete_trail(payload, trail_id):
  trail = Trail.query.get_or_404(trail_id)

  if trail:
    try:
      trail.delete()
      return jsonify({
        'success': True,
        'deleted': trail_id,
        'total_trails': len(Trail.query.all())
      })
    except Exception as error:
      abort(error.code)

#PATCH Trails
@api.route('trails/<int:trail_id>', methods=['PATCH'])
@requires_auth('patch:trails')
def update_trail(payload, trail_id):
  trail = Trail.query.get_or_404(trail_id)

  if trail:
    try:
      data = request.get_json()
      name = data.get('name', None)
      distance = data.get('distance', None)
      elevation = data.get('elevation', None)
      difficulty = data.get('difficulty', None)
      coordination = data.get('coordination', None)
      parking = data.get('parking', None)

      if not data:
        abort(400)
      if name:
        trail.name = name
      if distance:
        trail.distance = distance
      if elevation:
        trail.elevation = elevation
      if difficulty:
        trail.difficulty = difficulty
      if coordination:
        trail.coordination = json.dumps(coordination)
      if parking:
        trail.parking = parking
      
      trail.update()

      return jsonify({
        'success': True,
        'trail': [trail.format()]
      }), 200
    except Exception as error:
      abort(error.code)

#GET Reviews
@api.route('/reviews')
@requires_auth('get:reviews')
def get_reviews(payload):
  try:
    reviews = Review.query.all()
    reviews_list = paginate_items(request, reviews)

    if len(reviews_list) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'total_reviews': len(reviews_list),
      'reviews': reviews_list
    }), 200
  except Exception as error:
    print(error)
    return jsonify({
      'success': False,
      'error': str(error)
    }), 500

#POST Reviews
@api.route('/reviews', methods=['POST'])
@requires_auth('post:reviews')
def add_reviews(payload):
  body = request.get_json()

  rating = body.get('rating', None)
  comment = body.get('comment', None)
  user = body.get('user', None)
  trail_id = body.get('trail_id', None)

  try:
    new_review = Review(rating=rating, comment=comment, user=user, trail_id=trail_id)
    new_review.insert()

    return jsonify({
      'success': True,
      'created': new_review.id,
      'total_reviews': len(Review.query.all())
    })
  except Exception as error:
    abort(error.code)

#DELETE Reviews
@api.route('/reviews/<int:review_id>', methods=['DELETE'])
@requires_auth('delete:reviews')
def delete_review(payload, review_id):
  review = Review.query.get_or_404(review_id)

  if review:
    try:
      review.delete()
      return jsonify({
        'success': True,
        'deleted': review_id,
        'total_reviews': len(Review.query.all())
      })
    except Exception as error:
      abort(error.code)

#PATCH Reviews
@api.route('reviews/<int:review_id>', methods=['PATCH'])
@requires_auth('patch:reviews')
def update_review(payload, review_id):
  review = Review.query.get_or_404(review_id)

  if review:
    try:
      data = request.get_json()
      rating = data.get('rating', None)
      comment = data.get('comment', None)
      user = data.get('user', None)
      trail_id = data.get('trail_id', None)

      if not data:
        abort(400)
      if rating:
        review.rating = rating
      if comment:
        review.comment = comment
      if user:
        review.user = user
      if trail_id:
        review.trail_id = trail_id
      
      review.update()

      return jsonify({
        'success': True,
        'review': [review.format()]
      }), 200
    except Exception as error:
      abort(error.code)

## Error Handling
@api.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400

@api.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found'
    }), 404

@api.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method not allowed'
    }), 405

@api.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unable to process request'
    }), 422

@api.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
    }), 500

@api.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code