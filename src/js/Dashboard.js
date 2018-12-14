import React from "react";
import Gallery from "react-grid-gallery";

import axios from "axios";

export default class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      images: null
    };
    this.getImages = this.getImages.bind(this);
  }

  getImages() {
    axios.get("/wordclouds").then((res) => {
      const wordclouds = res.data.wordclouds;
      if (wordclouds.length > 0) {
        const images = wordclouds.map((key) => ({
          src: "https://eyedentity.s3.amazonaws.com/" + key,
          thumbnail: "https://eyedentity.s3.amazonaws.com/" + key,
          thumbnailWidth: 360,
          thumbnailHeight: 360,
          caption: key.replace(".png", "")
        }));
        this.setState({images});
      }
    });
  }

  componentDidMount() {
    this.getImages();
    const params = new URLSearchParams(location.search);
    console.log(params.get("interval"))
    const seconds = (params.get("interval") === null)
      ? 30
      : params.get("interval");
    setInterval(() => this.getImages(), seconds * 1000);

  }

  render() {
    const gallery = (this.state.images === null)
      ? "Loading..."
      : <Gallery images={this.state.images} enableImageSelection={false} backdropClosesModal={true} margin={5} showImageCount={false}/>;
    return (<div className="center">
      {gallery}
    </div>);
  }
}
