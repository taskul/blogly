tagsInput = document.querySelector('#post-tags')
tagsContainer = document.querySelector('.tag-container')
tagsForm = document.querySelector('.tags-input-form')
tagsDeleteButton = document.querySelectorAll('.delete-tag')

tagsForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (tagsInput.value.length > 1) {
        let label = document.createElement('label');
        let deleteTag = document.createElement('span');
        let tag = document.createElement('input');
        tag.setAttribute("type", "checkbox");
        tag.setAttribute("value", tagsInput.value);
        tag.setAttribute("checked", "checked");
        tag.setAttribute("name", "tags")
        tag.classList.add('tag-checkbox');
        deleteTag.textContent = 'X';
        label.textContent = tagsInput.value;
        deleteTag.classList.add('delete-tag')
        label.classList.add('tag');
        label.append(tag);
        label.append(deleteTag);
        tagsContainer.append(label);
        tagsInput.value = '';
    };
});

tagsContainer.addEventListener('click', async (e) => {
    if (e.target.tagName == 'SPAN') {
        let tag_id = e.target.getAttribute("data-tag_id")
        let post_id = e.target.getAttribute("data-post_id")
        await fetch('/posts/' + post_id + '/delete/' + tag_id, { method: 'DELETE' })
        e.target.parentElement.remove()
    }
})
