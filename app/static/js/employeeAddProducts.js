const BOOK_GERNE_API = '/api/v1/bookGerne'
const BOOK_API = '/api/v1/book/'

async function fetchGerne() {
    try {
        const res = await fetch(`${BOOK_GERNE_API}`)
        if (!res.ok) throw Error("Failed getting book gerne")
        const data = await res.json()
        return data['data']
    } catch (error) {
        alert(error.message)
    }
}

// New function to fetch all genres for initial load
async function fetchAllGenres() {
    try {
        // If you have a separate endpoint for all genres
        const res = await fetch(`${BOOK_GERNE_API}/all`)
        if (!res.ok) {
            // Fallback to the existing endpoint if /all doesn't exist
            const fallbackRes = await fetch(`${BOOK_GERNE_API}`)
            if (!fallbackRes.ok) throw Error("Failed getting all genres")
            const fallbackData = await fallbackRes.json()
            return fallbackData['data'] || fallbackData
        }
        const data = await res.json()
        return data['data'] || data
    } catch (error) {
        alert(error.message)
        return []
    }
}

// Function to populate the initial genre menu
async function loadInitialGenres() {
    try {
        const genres = await fetchAllGenres()
        const $col1 = $('#col1')

        // Clear existing content
        $col1.empty()

        // Handle both array and object responses
        const genreList = Array.isArray(genres) ? genres : (genres.genres || [])

        // Add each genre as a menu item
        genreList.forEach(genre => {
            const $menuItem = $('<div>')
                .addClass('menu-item')
                .attr('data-id', genre.book_gerne_id)
                .text(genre.name)  // Add this line to display the genre name
                .on('click', function() {
                    chooseCategory(genre.book_gerne_id, this)
                })

            $col1.append($menuItem)
        })

    } catch (error) {
        console.error('Error loading initial genres:', error)
        showToast('Failed to load genres', true)
    }
}


function showSpinner() {
    $('.spinner').show();
}

// HIDE SPINNER
function hideSpinner() {
    $('.spinner').hide();
}

async function fetchExtendAttribute(id) {
    try {
        const res = await fetch(`${BOOK_GERNE_API}/${id}/attributes`)
        if (!res.ok) throw Error("Failed getting book gerne")
        const data = await res.json()
        return data['data']
    } catch (error) {
        alert(error.message)
    }
}

const createBook = async function (data) {
    try {
        showSpinner()
        const res = await fetch(`${BOOK_API}`, {
            method: 'POST',
            body: data
        });
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const result = await res.json();
        return result
    } catch (error) {
        showToast(error.message, true)
    } finally {
        hideSpinner()
    }
}

const showToast = function (message, isError) {
    const color = isError ? 'var(--red)' : "#6cbf6c"
    Toastify({
        text: message,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
            background: color,
        }
    }).showToast()
}

let selectedPath = "";
let activeColumn1 = null;
let activeColumn2 = null;
let activeColumn3 = null;

let genres = [];
let fileImage = []

$(document).ready(function() {
    const $genreList = $("#genreList");
    const $genreSearch = $("#genreSearch");
    const $newGenreContainer = $("#newGenreContainer");
    const $newGenreInput = $("#newGenre");
    loadInitialGenres();
    // Publisher dropdown handler
    $('.dropdown-publisher .dropdown-item').on('click', function() {
        const $dropdownPublisher = $('.dropdown-toggle-publisher');
        $dropdownPublisher.attr('id', $(this).attr('value'));
        $dropdownPublisher.html(`<span class="ml-2">${$(this).text()}</span>`);
    });

    // Format dropdown handler
    $('.dropdown-format .dropdown-item').on('click', function() {
        const $dropdownFormat = $('.dropdown-toggle-format');
        $dropdownFormat.attr('id', $(this).attr('value'));
        $dropdownFormat.html(`<span class="ml-2">${$(this).text()}</span>`);
    });

    // Release date input formatting
    $('#release-date').on('input', function(e) {
        const $input = $(this);
        const value = $input.val();

        // Remove all non-numeric characters except '/'
        const sanitizedValue = value.replace(/[^0-9/]/g, '');

        // Automatically insert slashes for formatting
        if (sanitizedValue.length === 2 || sanitizedValue.length === 5) {
            $input.val(sanitizedValue + '/');
        } else {
            $input.val(sanitizedValue);
        }
        // Limit length to 10 characters (dd/mm/yyyy)
        if (sanitizedValue.length > 10) {
            $input.val(sanitizedValue.slice(0, 10));
        }
    });

    // Release date validation on blur
    $('#release-date').on('blur', function(e) {
        const $input = $(this);
        const value = $input.val();

        // Regular expression for dd/mm/yyyy format
        const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/;

        if (!dateRegex.test(value)) {
            $('#errorMessage').show();
        } else {
            $('#errorMessage').text('');

            // Optional: Additional validation for actual date
            const [_, day, month, year] = value.match(dateRegex);

            const date = new Date(`${year}-${month}-${day}`);
            if (
                date.getFullYear() !== parseInt(year) ||
                date.getMonth() + 1 !== parseInt(month) ||
                date.getDate() !== parseInt(day)
            ) {
                $('#errorMessage').text('Invalid date!');
            }
        }
    });

    // Prevent default button actions
    $('button').on('click', function(event) {
        event.preventDefault();
    });

    // Modal overlay click handler
    $("#modalOverlay").on("click", function(event) {
        if (event.target === this) {
            closeModal();
        }
    });

    // Genre search focus handler
    $genreSearch.on("focus", function() {
        populateGenreList();
        $genreList.show();
    });

    // Genre search input handler
    $genreSearch.on("input", function() {
        populateGenreList($genreSearch.val());
    });

    // Hide dropdown when clicking outside
    $(document).on("click", function(event) {
        if (!$(event.target).closest(".dropdown-container").length) {
            $genreList.hide();
        }
    });

    // File upload handler
    $('#book-image').on('change', function () {
        const $container = $('.image-list');
        const $uploadBox = $('.upload-box-image');
        const files = Array.from(this.files);

        // Clear previous images
        $container.empty();
        fileImage = [];

        const file = files[0]; // Only one image allowed

        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = e => {
                const html = `
                    <div id='image-0' class="image-item position-relative">
                        <img class="w-100 h-100" src="${e.target.result}">
                        <button onclick="handleRemoveImage(event, 'image-0')" class="btn text-primary btn-delete-image">
                            <i class="fa-solid fa-x"></i>
                        </button>
                    </div>
                `;
                $container.append(html);
                $uploadBox.hide(); // Hide upload button
            };
            reader.readAsDataURL(file);
            fileImage.push(file);
        } else {
            alert(`${file.name} is not a valid image file.`);
        }

        // Allow re-selecting same file
        $(this).val('');
    });



    // Form submission handler
    $('.btn-create-book').on('click', function(e) {
        handleCreateBook(e);
    });
});

function openModal() {
    $("#modalOverlay").addClass("active");
}

function closeModal() {
    $("#modalOverlay").removeClass("active");
    selectedPath = '';
    if (activeColumn1) {
        $(activeColumn1).removeClass("active");
        activeColumn1 = null;
    }
    updateSelectedDisplay();
}

function updateSelectedDisplay() {
    $("#selectedPath").text(selectedPath);
}

async function chooseCategory(id, element) {
    $('.menu-item').removeClass('active')
    $('.menu-item').attr("id", id);

    $(element).addClass('active')

    console.log('Selected genre ID:', id)
}

async function confirmSelection() {
    try {
        let gerneId;
        const $menuItem = $("#col1 .menu-item.active")
        if ($menuItem.length) {
            gerneId = $menuItem.attr('id');
        } else {
            throw new Error("Vui lòng chọn thể loại cụ thể");
        }

        $('input[name="input-gerne"]').attr('data-id', gerneId);
        $('input[name="input-gerne"]').val($menuItem.text());
    } catch (error) {
        showToast(error.message, true);
    }
    closeModal();
}

function filterMenuItems() {
    const searchInput = $("#searchInput").val().toLowerCase();
    $(".menu-item").each(function() {
        const text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(searchInput));
    });
}

async function populateGenreList(filter = "") {
    const $genreList = $("#genreList");
    $genreList.empty();

    const filteredGenres = genres.filter(genre =>
        genre['attribute_name'].toLowerCase().includes(filter.toLowerCase())
    );

    filteredGenres.forEach(genre => {
        const $item = $('<div>')
            .addClass("dropdown-item")
            .attr('id', genre['attribute_id'])
            .text(genre['attribute_name'])
            .on('click', function() {
                addExtendAttribute(genre['attribute_id'], genre['attribute_name']);
            });
        $genreList.append($item);
    });
    $genreList.show();
}

// function handleRemoveImage(e, name) {
//     e.preventDefault();
//     const $container = $('.image-list');
//     fileImage.splice(parseInt(name.split('-')[1]), 1);
//     $container.find(`#${name}`).remove();
// }
// Image remove handler
function handleRemoveImage(event, imageId) {
    event.preventDefault();
    $('#' + imageId).remove();
    fileImage = [];
    $('.upload-box-image').show(); // Show upload again
}

function clearValue() {
    $('input[name="title"]').val('');
    $('input[name="input-gerne"]').attr('id', '');
    $("#product-description").val('');
    $('input[name="product-author"]').val('');
    $('input[name="product-num-page"]').val('');
    $('.dropdown-toggle-publisher').attr('id', '').text('');
    $('.dropdown-toggle-format').attr('id', '').text('');
    $('input[name="release-date"]').val('');
    $('input[name="product-price"]').val('');
    $('input[name="product-weight"]').val('');
    $('input[name="product-dimension-r"]').val('');
    $('input[name="product-dimension-d"]').val('');
    $('input[name="product-dimension-c"]').val('');
    $('.group-extend-atrtribute').empty();
    $('.image-list').empty();
    fileImage = [];
}

function handleCreateBook(e) {
    try {
        const title = $('input[name="title"]').val().trim();
        const gerneId = $('input[name="input-gerne"]').attr('data-id');
        const description = $("#product-description").val()?.trim();
        const author = $('input[name="product-author"]').val()?.trim();
        const num_page = $('input[name="product-num-page"]').val();
        const publisher = $('.dropdown-toggle-publisher').attr('id');
        const format = $('.dropdown-toggle-format').attr('id');
        const releaseDate = $('input[name="release-date"]').val();
        const quantity = $('input[name="product-price"]').val();
        const weight = $('input[name="product-weight"]').val();
        const r = $('input[name="product-dimension-r"]').val();
        const d = $('input[name="product-dimension-d"]').val();
        const c = $('input[name="product-dimension-c"]').val();
        const barcode = $('input[name="product-barcode"]').val();

        let flag = false;

        // Validation with jQuery
        if (!fileImage.length) {
            flag = true;
            $('#error-image').addClass('text-primary');
        } else {
            $('#error-image').removeClass('text-primary');
        }

        if (title === '') {
            flag = true;
            $('#error-title').addClass('text-primary');
        } else {
            $('#error-title').removeClass('text-primary');
        }
        console.log("gerne Id", gerneId)
        if (!gerneId) {
            flag = true;
            $('#error-gerne').addClass('text-primary');
        } else {
            $('#error-gerne').removeClass('text-primary');
        }

        if (description === '') {
            flag = true;
            $('#error-description').addClass('text-primary');
        } else {
            $('#error-description').removeClass('text-primary');
        }

        if (author === '') {
            flag = true;
            $('#error-author').addClass('text-primary');
        } else {
            $('#error-author').removeClass('text-primary');
        }

        if (num_page === '') {
            flag = true;
            $('#error-num-pages').addClass('text-primary');
        } else {
            $('#error-num-pages').removeClass('text-primary');
        }

        if (quantity === '') {
            flag = true;
            $('#error-price').addClass('text-primary');
        } else {
            $('#error-price').removeClass('text-primary');
        }

        if (weight === '') {
            flag = true;
            $('#error-weight').addClass('text-primary');
        } else {
            $('#error-weight').removeClass('text-primary');
        }

        if (r === '' || d === '' || c === '') {
            flag = true;
            $('#error-dimessions').addClass('text-primary');
        } else {
            $('#error-dimessions').removeClass('text-primary');
        }

        if (barcode === '' || isNaN(barcode) || barcode.length !== 12) {
            throw new Error("Sai định dạng barcode UPC 8");
        } else {
            $('#error-barcode').removeClass('text-primary');
        }

        if (flag) throw Error("Vui lòng nhập các trường cần thiết");

        const data = {
            'title': title,
            'book_gerne_id': gerneId,
            'author': author,
            'quantity': quantity,
            'num_page': num_page,
            'description': description,
            'format': format,
            'weight': weight,
            'publisher': publisher,
            'release_date': releaseDate,
            'dimension': r + 'x' + d + 'x' + c + ' cm',
            'book_images': fileImage,
            'barcode': barcode
        };

        const formData = new FormData();
        for (const key in data) {
            if (data.hasOwnProperty(key)) {
                if (key === 'book_images' && Array.isArray(data[key])) {
                    data[key].forEach(file => {
                        formData.append('book_images[]', file);
                    });
                } else {
                    formData.append(key, data[key]);
                }
            }
        }

        e.preventDefault();
        createBook(formData).then(res => {
            if (res['status'] === 200) {
                showToast("Tạo sách thành công ", false);
                clearValue();
                $('html, body').animate({ scrollTop: 0 }, 'smooth');
            }
        }).then(() => {
            window.location.reload();
        });

    } catch (error) {
        showToast(error.message, true);
    }
}