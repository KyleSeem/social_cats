
// called by jquery when an image file input change occurs
// used to read file and resize (if necessary) before sending to server
var myReaderFunction = function(file, canvasId, modalId, urlFieldId) {
    // Load the image
    var reader = new FileReader();
    reader.onload = function (readerEvent) {
        // var exif = EXIF.readFromBinaryFile(new BinaryFile(this.result));

        var image = new Image();
        image.onload = function (imageEvent) {
            var width;
            var height;
            var max_size = 600;
            var max_width = (screen.width * .9);
            var max_height = screen.height * .75;
            var canvas = document.getElementById(canvasId);

            // get image exif tags
            EXIF.getData(image, function() {
                exif = EXIF.getTag(this, "Orientation");
                console.log('EXIF', exif);
            });

            console.log('original image', image.width, image.height);


            // resize image
            if (image.width > image.height) {
                if (image.width > max_size) {
                    image.height *= max_size / image.width;
                    image.width = max_size;
                }
            } else {
                if (image.height > max_size) {
                    image.width *= max_size / image.height;
                    image.height = max_size;
                }
            }
            console.log('new image', image.width, image.height);

    // cropperjs functions to create and size [replacement] canvas don't scale well after resizing the image
    // this results in a modal that is too big for the screen that will not scroll
    // before defining the w/h of the canvas, check the screen dimensions and scale appropriately for a better fit

            // if image is bigger than screen
            if (max_size >= screen.width) {
                // if image is a square
                if (image.width == image.height) {
                    width = max_width;
                    height = max_width;
                }
                // if image is not a square
                else {
                    // if exif = 1-4 or undefined (canvas height/width do not need to be swapped)
                    if (exif <= 4 || exif == 'undefined') {
                        height = image.height * (max_width / image.width);
                        width = max_width;
                        // if image is portrait shrink a little so modal fits better
                        if (height > width) {
                            height *= .85;
                            width *= .85;
                        }
                    }
                    // if exif = 5-8 (canvas height/width needs to be swapped before drawing)
                    else {
                        console.log('iw, ih', image.width, image.height)
                        width = image.width * (max_width / image.height);
                        height = max_width;
                        // reversed for exif 5-8
                        if (width > height) {
                            height *= .85;
                            width *= .85;
                        }
                    }
                }
            // if image is not bigger than screen
            } else {
                height = image.height;
                width = image.width;
            }
            
            // define canvas width and height
            canvas.width = width;
            canvas.height = height;


            var context = canvas.getContext('2d');
            // find correct exif tag and transform context accordingly
            switch(exif) {
                // case 1 = default: (1,0,0,1,0,0)
                case 2:
                    context.transform(-1, 0, 0, 1, width, 0);
                    break;
                case 3:
                    context.transform(-1, 0, 0, -1, width, height);
                    break;
                case 4:
                    context.transform(1, 0, 0, -1, 0, height);
                    break;
                case 5:
                    canvas.width = height;
                    canvas.height = width;
                    context.transform(0, 1, 1, 0, 0, 0);
                    break;
                case 6:
                    canvas.width = height;
                    canvas.height = width;
                    context.setTransform(0, 1, -1, 0, height, 0);
                    break;
                case 7:
                    canvas.width = height;
                    canvas.height = width;
                    context.transform(0, -1, -1, 0, height , width);
                    break;
                case 8:
                    canvas.width = height;
                    canvas.height = width;
                    context.transform(0, -1, 1, 0, 0, width);
                    break;

            }
            // render context to canvas
            context.drawImage(image, 0, 0, width, height);
            console.log('final image', image.width, image.height);


            var dataUrl = canvas.toDataURL('image/jpeg');
            var resizedImage = dataURLToBlob(dataUrl);
            $.event.trigger({
                type: "imageResized",
                blob: resizedImage,
                url: dataUrl,
                modalId: modalId,
                urlFieldId: urlFieldId
            });
        }
        image.src = readerEvent.target.result;
    }
    reader.readAsDataURL(file);
};


// Utility function to convert a canvas to a BLOB
var dataURLToBlob = function(dataURL) {
    var BASE64_MARKER = ';base64,';
    if (dataURL.indexOf(BASE64_MARKER) == -1) {
        var parts = dataURL.split(',');
        var contentType = parts[0].split(':')[1];
        var raw = parts[1];

        return new Blob([raw], {type: contentType});
    }

    var parts = dataURL.split(BASE64_MARKER);
    var contentType = parts[0].split(':')[1];
    var raw = window.atob(parts[1]);
    var rawLength = raw.length;

    var uInt8Array = new Uint8Array(rawLength);

    for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], {type: contentType});
};
