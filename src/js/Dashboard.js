import React from 'react';
import Gallery from 'react-grid-gallery';

import axios from 'axios';

export default class Dashboard extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      images: null
    }
  }

  componentDidMount() {
    axios.get('/wordclouds').then(res => {
      const wordclouds = res.data.wordclouds;
      if (wordclouds.length > 0) {
        const images = wordclouds.map((key) => ({
          src: "https://eyedentity.s3.amazonaws.com/" + key,
          thumbnail: "https://eyedentity.s3.amazonaws.com/" + key,
          thumbnailWidth: 240,
          thumbnailHeight: 240
        }))
        this.setState({images});
      }
    })
  }

  render() {
    const gallery = (this.state.images === null)
      ? "Loading..."
      : <Gallery images={this.state.images} enableImageSelection={false} backdropClosesModal={true}/>
    return (<div>
      <div style={{
          justifyContent: 'center',
          padding: 50
        }}>
        {gallery}
      </div>
    </div>)
  }
}
