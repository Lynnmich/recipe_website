'''# Render template for adding a new category
@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(
                name=form.name.data
            )
        
        # Clear the form after submission
        form.name.data = ''

        # Add data to the database
        db.session.add(category)
        db.session.commit()

        # Return a message once submission is successful
        flash("Category submitted successfully!")

    # Redirect back to the webpage
    return render_template("add_category.html", form=form)


# List all categories in databases
@app.route('/categories')
def categories():
    page = get_page()
    categories = Category.query.order_by(Category.id)
    pagination = Pagination(page=page, total=categories.count(),
                            record_name='categories')
    category_list = paginate_list(categories, page, 10)
    return render_template('categories.html', categories=categories,
                           pagination=pagination)


# Editing categories to the database
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data

        # Commit changes to the database
        db.session.add(category)
        db.session.commit()

        flash("Category has been updated successfully!")
        return redirect(url_for("category", id=category.id))

    form.name.data = category.name
    return render_template('edit_category.html', form=form)

# Deleting categories from the database
@app.route('/categories/delete/<int:id>')
def delete_category(id):
    category_delete = Category.query.get_or_404(id)

    try:
        db.session.delete(category_delete)
        db.session.commit()

        flash("Category deleted!")

        # Return all categories from the db
        categories = Category.query.order_by(Category.id)
        return render_template("categories.html", categories=categories)

    except:
        # Error message
        flash("There was a problem deleting the category")

        # Return all categories from the db
        categories = Category.query.order_by(Category.id)
        return render_template("categories.html", categories=categories)'''


'''# Render template for adding a new category
@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(
            name=form.name.data
        )

        # Clear the form after submission
        form.name.data = ''

        # Add data to the database
        db.session.add(category)
        db.session.commit()

        # Return a message once submission is successful
        flash("Category added successfully!")

    # Redirect back to the webpage
    return render_template("add_category.html", form=form)

# List all categories in the database
@app.route('/categories')
def categories():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    # Query all 
    query = Category.query


    # Count the total number
    total = query.count()

    # Paginate the query
    categories = query.order_by(Category.id).offset(offset).limit(per_page).all()

    # Create a Pagination object
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')

    return render_template("categories.html", categories=categories, pagination=pagination)

# Display recipes by category
@app.route('/categories/<int:id>')
def recipes_by_category(id):
    category = Category.query.get_or_404(id)
    recipes = Recipe.query.filter_by(category_id=id).all()
    return render_template('recipes_by_category.html', recipes=recipes)'''