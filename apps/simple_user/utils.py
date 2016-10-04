def get_breadcrumb(id, model, parent_field):
    breadcrumb = []
    sel = model.get(id=id)
    sel.click_count += 1
    sel.save()
    breadcrumb.append(sel.name)
    while getattr(sel, parent_field):
        sel = model.get(id=getattr(sel, parent_field))
        breadcrumb.append(sel.name)
        sel.click_count += 1
        sel.save()
    breadcrumb = breadcrumb[::-1]
    return ' -> '.join(breadcrumb)


emoji_pool = ['❤', '💋', '😡', '👿', '🤖', '💀', '👻', '👽', '💩', '💤', '😼', '👀', '😼', '👕', '👗', '🌂', '🐨',
              '🐝', '🐴', '🐟', '🌳', '🌵', '🍀', '☀', '🌎', '🌸', '🍎', '🍔', '🍪', '🎂', '⚽', '🏀', '🏹',
              '⛸', '🎻', '🎯', '🎲', '🎪', '🎖', '🚲', '🚀', '🚤', '🚁', '🏁', '🚥', '🏛', '🎈', '🎀', '💌', '📨', '📙',
              '📎', '✂', '💛', '💚', '💙', '💜', '💔', '⭕', '❌', '🚫', '✅', '➕']
# Even if you cant see them, they are here
