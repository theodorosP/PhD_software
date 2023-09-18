#This function merges two images vertically, 
#img1 and img2 are the two images we want to merge

def merge_images_vericaly(img1, img2):
  from PIL import Image
  import matplotlib.image as mpimg
  # Load the two PNG images
  image1 = Image.open(img1)
  image2 = Image.open(img2)

  # Calculate the total width and height for the merged image
  total_width = max(image1.width, image2.width)
  total_height = image1.height + image2.height

  # Create a blank merged image
  merged_image = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))

  # Paste the first image at the top and the second image at the bottom
  merged_image.paste(image1, (0, 0))
  merged_image.paste(image2, (0, image1.height))

  # Save the merged image
  merged_image.save("merged_image.png")

  # Close the images
  image1.close()
  image2.close()

  #dispaly merged image
  img = mpimg.imread("merged_image.png")
  plt.axis("off")
  plt.imshow(img)
